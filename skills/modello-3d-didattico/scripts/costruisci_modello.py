#!/usr/bin/env python3
"""Costruisce il diorama 3D a partire da meta.json + tex/ ed esporta il GLB.

Composizione (dal fondo verso chi guarda):
  - gradino rialzato con le scene in creta, ESTRUSE dalla sagoma reale
  - freccia 3D con le sfere dorate, una per evento
  - targhette inclinate con anno e nome dell'evento
  - basamento a due livelli

Nessun hotspot: il modello e' puramente espositivo. L'interazione (es.
bandiere da posizionare) vive nella scena di realta' virtuale (Figmin XR).

Uso:
  python3 costruisci_modello.py [--meta meta.json] [--tex tex] [--src-w 1376]
      [--px 0.0199] [--fig-t 0.42] [--label-tilt 52] [--insegna]
      [--out linea_del_tempo_3d.glb]
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import cv2
import numpy as np
import trimesh
from PIL import Image
from shapely.geometry import LineString, Polygon
from shapely.ops import unary_union
from trimesh.transformations import rotation_matrix

COL = {
    "viola":    [0x60, 0x30, 0x90, 255],
    "viola_sc": [0x46, 0x20, 0x6c, 255],
    "oro":      [0xc9, 0xa2, 0x27, 255],
    "noce":     [0x4a, 0x2f, 0x21, 255],
    "pergam":   [0xef, 0xe3, 0xcd, 255],
    "gradino":  [0xe1, 0xd0, 0xaf, 255],
}


def pbr(color=None, texture=None, rough=0.85, metal=0.0, mask=False):
    kw = dict(metallicFactor=metal, roughnessFactor=rough, doubleSided=False)
    if color is not None:
        kw["baseColorFactor"] = color
    if texture is not None:
        kw["baseColorTexture"] = texture
        kw["alphaMode"] = "MASK" if mask else "OPAQUE"
        if mask:
            kw["alphaCutoff"] = 0.4
    return trimesh.visual.material.PBRMaterial(**kw)


def solid(mesh, color, rough=0.85, metal=0.0):
    mesh.visual = trimesh.visual.TextureVisuals(
        material=pbr(color=color, rough=rough, metal=metal))
    return mesh


SS = 4          # sovracampionamento del contorno: bordi lisci, non a scalini


def polygons_from_alpha(png_path, thr=110):
    img = Image.open(png_path).convert("RGBA")
    W, H = img.size
    alpha = np.asarray(img)[..., 3]
    mask = ((alpha > thr).astype(np.uint8)) * 255
    k3 = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k3, iterations=2)
    # ingrandisco, sfumo e risoglio: il contorno esce curvo invece che a gradini
    mask = cv2.resize(mask, (W * SS, H * SS), interpolation=cv2.INTER_CUBIC)
    mask = cv2.GaussianBlur(mask, (2 * SS + 1, 2 * SS + 1), 0)
    mask = ((mask > 127).astype(np.uint8)) * 255

    cnts, hier = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    if hier is None:
        raise RuntimeError(f"nessun contorno in {png_path}")
    hier = hier[0]
    a_min = 55 * SS * SS
    polys = []
    for i, c in enumerate(cnts):
        if hier[i][3] != -1 or cv2.contourArea(c) < a_min or len(c) < 4:
            continue
        holes = []
        j = hier[i][2]
        while j != -1:
            if cv2.contourArea(cnts[j]) > a_min * 0.8 and len(cnts[j]) >= 4:
                holes.append(cnts[j][:, 0, :].astype(float) / SS)
            j = hier[j][0]
        p = Polygon(c[:, 0, :].astype(float) / SS, holes)
        if not p.is_valid:
            p = p.buffer(0)
        if p.is_empty:
            continue
        for g in (p.geoms if p.geom_type == "MultiPolygon" else [p]):
            if g.geom_type == "Polygon" and not g.is_empty:
                polys.append(g)
    return polys, W, H


def extruded_from_png(png_path, world_h, thickness, erode_px=0.5,
                      simp_px=1.0, mask_alpha=True, rough=0.9):
    """Estrude la sagoma del PNG; restituisce la mesh centrata in X e con la
    base della sagoma a quota 0, cosi' l'oggetto appoggia davvero."""
    polys, W, H = polygons_from_alpha(png_path)
    s = world_h / H
    off_x = W * s / 2.0

    parts = []
    for p in polys:
        q = Polygon(
            [(x * s - off_x, (H - y) * s) for x, y in p.exterior.coords],
            [[(x * s - off_x, (H - y) * s) for x, y in r.coords]
             for r in p.interiors])
        q = q.buffer(-erode_px * s).simplify(simp_px * s)
        if q.is_empty:
            continue
        for g in (q.geoms if q.geom_type == "MultiPolygon" else [q]):
            if g.is_empty or g.area < (2.5 * s) ** 2:
                continue
            try:
                parts.append(trimesh.creation.extrude_polygon(g, height=thickness))
            except Exception:
                continue
    if not parts:
        raise RuntimeError(f"estrusione fallita: {png_path}")

    mesh = trimesh.util.concatenate(parts)
    mesh.apply_translation([0, 0, -thickness / 2.0])
    foot = float(mesh.bounds[0][1])
    mesh.apply_translation([0, -foot, 0])

    # UV proiettate: trimesh capovolge la V in esportazione, quindi la
    # fornisco gia' con l'origine in basso.
    v = mesh.vertices
    uv = np.column_stack([(v[:, 0] + off_x) / (W * s),
                          (v[:, 1] + foot) / (H * s)])
    mesh.visual = trimesh.visual.TextureVisuals(
        uv=uv, material=pbr(texture=Image.open(png_path).convert("RGBA"),
                            rough=rough, mask=mask_alpha))
    return mesh


def build(cfg: dict, meta: dict, tex: str) -> trimesh.Scene:
    SRC_W = float(cfg["src_w"])
    PX = float(cfg["px"])
    SPAN = SRC_W * PX
    UP = int(meta.get("up", 1))
    FIG_H = (meta["band_h"] / UP) * PX
    FIG_T = float(cfg["fig_t"])
    CON_INSEGNA = bool(cfg["insegna"])

    BASE_W, BASE_H, BASE_D = SPAN + 1.6, 0.80, 7.6
    PLINTH_W, PLINTH_H, PLINTH_D = SPAN + 2.4, 0.50, 8.9
    Z_BASE = 0.15
    RISER_W, RISER_H, RISER_D = SPAN + 0.8, 1.00, 2.10
    Z_RISER, Z_FIG = -2.10, -2.10
    Z_ARROW, Z_LABEL, Z_TITLE = 1.00, 3.35, -4.10

    LABEL_W = float(cfg["label_w"])
    LABEL_H = LABEL_W / 2.0
    LABEL_TILT = float(cfg["label_tilt"])

    R_SHAFT = 25 * PX
    R_HEAD = 50 * PX
    AR_T = float(cfg["fig_t"]) + 0.20 if cfg.get("ar_t") is None else float(cfg["ar_t"])

    def x_of(pct):
        return (pct / 100.0 - 0.5) * SPAN

    X_START = x_of(2.5)
    X_HEADBASE = x_of(92.6)
    X_TIP = x_of(97.5)

    sc = trimesh.Scene()

    def add(mesh, name):
        sc.add_geometry(mesh, geom_name=name, node_name=name)

    # basamento
    m = trimesh.creation.box(extents=[PLINTH_W, PLINTH_H, PLINTH_D])
    m.apply_translation([0, -BASE_H - PLINTH_H / 2, Z_BASE])
    add(solid(m, COL["noce"], rough=0.7), "zoccolo")

    m = trimesh.creation.box(extents=[BASE_W, BASE_H, BASE_D])
    m.apply_translation([0, -BASE_H / 2, Z_BASE])
    add(solid(m, COL["pergam"], rough=0.95), "basamento")

    # gradino su cui poggiano le scene
    m = trimesh.creation.box(extents=[RISER_W, RISER_H, RISER_D])
    m.apply_translation([0, RISER_H / 2, Z_RISER])
    add(solid(m, COL["gradino"], rough=0.95), "gradino")

    # freccia piatta: asta a capo tondo + punta triangolare, in un pezzo solo
    shaft = LineString([(X_START, 0), (X_HEADBASE, 0)]).buffer(
        R_SHAFT, cap_style=1, resolution=24)
    head = Polygon([(X_HEADBASE - 0.02, R_HEAD), (X_TIP, 0),
                    (X_HEADBASE - 0.02, -R_HEAD)])
    plan = unary_union([shaft, head])
    plan = Polygon([(x, -z) for x, z in plan.exterior.coords])
    m = trimesh.creation.extrude_polygon(plan, height=AR_T)
    m.apply_transform(rotation_matrix(-np.pi / 2, [1, 0, 0]))
    m.apply_translation([0, 0, Z_ARROW])
    add(solid(m, COL["viola"], rough=0.55), "freccia")

    m = trimesh.creation.extrude_polygon(plan.buffer(0.07), height=0.10)
    m.apply_transform(rotation_matrix(-np.pi / 2, [1, 0, 0]))
    m.apply_translation([0, 0, Z_ARROW])
    add(solid(m, COL["viola_sc"], rough=0.6), "freccia_zoccolo")

    # scene, sfere dorate, targhette
    centers = [f["center_pct"] for f in meta["figures"]]
    for i, fig in enumerate(meta["figures"]):
        x = x_of(centers[i])

        m = extruded_from_png(os.path.join(tex, fig["file"]), FIG_H, FIG_T)
        m.apply_translation([x, RISER_H, Z_FIG])
        add(m, f"scena_{i}_{meta['events'][i][0]}")

        m = trimesh.creation.icosphere(subdivisions=3, radius=0.32)
        m.apply_translation([x, AR_T + 0.10, Z_ARROW])
        add(solid(m, COL["oro"], rough=0.3, metal=0.6), f"sfera_{i}")

        m = extruded_from_png(os.path.join(tex, f"label_{i}.png"), LABEL_H,
                              0.11, erode_px=0.4, simp_px=0.35, rough=0.8)
        T = rotation_matrix(np.deg2rad(-LABEL_TILT), [1, 0, 0])
        T[:3, 3] = [x, 0.02, Z_LABEL]
        m.apply_transform(T)
        add(m, f"targa_{i}_{meta['events'][i][0]}")

    # insegna del titolo (opzionale: --insegna)
    if CON_INSEGNA:
        title_h = 3.30
        title_w = title_h * 4.0                # texture 2048x512
        title_y = RISER_H + FIG_H + 0.45
        m = extruded_from_png(os.path.join(tex, "title.png"), title_h, 0.18,
                              erode_px=0.4, simp_px=0.35, rough=0.8)
        m.apply_translation([0, title_y, Z_TITLE])
        add(m, "titolo")

        post_x = title_w / 2 + 0.40
        h_post = title_y + title_h + 0.30
        for k, sx in enumerate((-post_x, post_x)):
            m = trimesh.creation.box(extents=[0.34, h_post, 0.34])
            m.apply_translation([sx, h_post / 2, Z_TITLE - 0.05])
            add(solid(m, COL["noce"], rough=0.7), f"montante_{k}")
            cap = trimesh.creation.icosphere(subdivisions=3, radius=0.24)
            cap.apply_translation([sx, h_post + 0.12, Z_TITLE - 0.05])
            add(solid(cap, COL["oro"], rough=0.3, metal=0.6), f"pomolo_{k}")

        for k, yy in enumerate((title_y + 0.30, title_y + title_h - 0.30)):
            rail = trimesh.creation.box(extents=[2 * post_x, 0.18, 0.18])
            rail.apply_translation([0, yy, Z_TITLE - 0.14])
            add(solid(rail, COL["noce"], rough=0.7), f"traversa_{k}")

    return sc


def main() -> None:
    ap = argparse.ArgumentParser(description="Costruisci il diorama 3D ed esporta il GLB")
    ap.add_argument("--meta", default="meta.json")
    ap.add_argument("--tex", default="tex")
    ap.add_argument("--src-w", type=float, default=1376.0)
    ap.add_argument("--px", type=float, default=0.0199, help="Scala unità/pixel")
    ap.add_argument("--fig-t", type=float, default=0.42, help="Spessore scene")
    ap.add_argument("--ar-t", type=float, default=None, help="Spessore freccia (default: fig-t+0.20)")
    ap.add_argument("--label-w", type=float, default=2.86)
    ap.add_argument("--label-tilt", type=float, default=52.0, help="Inclinazione targhette (gradi)")
    ap.add_argument("--insegna", action="store_true", help="Includi l'insegna del titolo")
    ap.add_argument("--out", default="linea_del_tempo_3d.glb")
    args = ap.parse_args()

    meta = json.loads(Path(args.meta).read_text(encoding="utf-8"))
    cfg = dict(src_w=args.src_w, px=args.px, fig_t=args.fig_t, ar_t=args.ar_t,
               label_w=args.label_w, label_tilt=args.label_tilt,
               insegna=args.insegna)
    scene = build(cfg, meta, args.tex)
    scene.export(args.out)
    tris = sum(len(g.faces) for g in scene.geometry.values())
    b = np.round(scene.bounds, 2)
    print("geometrie:", len(scene.geometry), "| triangoli:", tris)
    print("dimensioni  X:", round(b[1][0] - b[0][0], 2),
          " Y:", round(b[1][1] - b[0][1], 2),
          " Z:", round(b[1][2] - b[0][2], 2))
    print("GLB:", args.out, os.path.getsize(args.out) // 1024, "KB")


if __name__ == "__main__":
    main()

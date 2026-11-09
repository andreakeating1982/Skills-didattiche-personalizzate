# Riferimenti rapidi — Lingue Facili

## Comandi

```bash
cd /home/user/lingue-facili
pnpm check        # tsc --noEmit
pnpm build        # build produzione
pnpm dev          # dev server (http://localhost:3000)
pnpm drizzle-kit push   # schema DB (usare QUESTO: db:push/db:reset falliscono)
```

## Struttura del file languages.ts (estratto)

```
export type LangCode = "en" | "fr" | "es";
export const LANG_CODES: LangCode[] = ["en", "fr", "es"];
export const LANG_LABELS: Record<LangCode, { nome: string; flag: string }> = {...};
export const LANG_ACCENT: Record<LangCode, string> = {...};   // colore accent per lingua
export const LANGS: Record<LangCode, LangConfig> = { en: EN, fr: FR, es: ES };
export function langConfig(lang?: string | null): LangConfig;
```

`LangConfig` contiene (order ~200 righe per lingua, copiare EN come base): appTitle, sottotitolo, welcomeTesti, cropHint, typeCards (mc/tf/mi/mc2/reorder: en/it/how), placeholder testo e focus, feedbackOK/KO, checkBtn, colTarget, istruzioni PDF, prompt AI persona+esempi, dizionario fallback e parole concrete.

## Asset in produzione

- App: https://lingue-facili.easy-peasy.site
- Font OpenDyslexic: https://lingue-facili.easy-peasy.site/fonts/OpenDyslexic-{Regular,Bold}-v2.woff2 (200)
- Modelli OCR: https://lingue-facili.easy-peasy.site/tessdata/{eng,fra,spa}.traineddata.gz
- Immagine diorama: https://media.easy-peasy.ai/2a7acf3f-cca7-4d59-aad6-6932daf36e1b/2b862452-99a4-4b26-92da-415a0702758a.png (stile claymation di Inglese/Francese Facile: libro aperto «LINGUE FACILI», bolle Hello!/Bonjour!/¡Hola!, Big Ben + Eiffel + monumento spagnolo, 6 bandiere, calamo; ortografia verificata lettera per lettera)

## Test del rilevatore di lingua (ASCOLTO)

```bash
python3 - <<'EOF'
src = open('/home/user/lingue-facili/client/src/hooks/useReadAloud.ts').read()
body = src[src.index('export type LangTts'):src.index('// ─', src.index('function detectLanguage'))]
tests = '''
const casi = [
  ["Maria es una estudiante de Madrid.", "es", undefined],
  ["Todos los días ella se levanta.", "es", "en"],
  ["She gets up every day at seven.", "en", undefined],
  ["Le matin, elle prend le petit déjeuner.", "fr", undefined],
  ["Elle se lève tous les jours.", "fr", "es"],
  ["Minimo 20 caratteri: inserisci il testo.", "it", "fr"],
  ["Maria is a student in Madrid.", "en", "es"],
  ["¡Hola! ¿Cómo estás?", "es", "fr"],
];
let fail = 0;
for (const [t, expected, prefer] of casi) {
  const got = detectLanguage(t, prefer as any);
  if (got !== expected) { fail++; console.log("FAIL", prefer, expected, got, t); }
}
console.log(fail === 0 ? "TUTTI OK" : fail + " FALLITI");
'''
open('/tmp/detect-test.ts','w').write(body + tests)
EOF
node --experimental-strip-types /tmp/detect-test.ts
```

## Q&A note

Il `[Auth] Authentication failed: HttpError: Not authenticated` 403 nel log server è RUMORE benigno (context.ts tenta il login su ogni richiesta; le procedure exercises sono publicProcedure): identico alle app sorelle, non correggere.

## Sorelle da allineare in UI

Stesso stile di Shakespeare Quiz/Latino Facile: barra accessibilità 5 moduli (FONT, INTERLINEA, RIGHELLO, MODALITÀ, ASCOLTO), OpenDyslexic auto-ospitato, classi `lf-welcome-top/lf-embedded` + `heightSync`, palette carta #f8f1e4 / inchiostro #2e2018 / barre #fdfbf8 / capsule #f5f0e6 / bordi #dedbd6.

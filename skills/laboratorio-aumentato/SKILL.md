---
name: laboratorio-aumentato
description: "Manutenzione e personalizzazione dell'app Laboratorio Aumentato (Vite + React + TypeScript + Tailwind + tRPC + Drizzle + SQLite). Usare per: modificare UI studente/docente, allineare stili a Shakespeare Quiz, deploy preview/produzione, personalizzare report PDF, rinominare l'app. L'app condivide la codebase scaffold con Shakespeare Quiz ma ha UI e palette colori distinte (plum, gold, success)."
---

# Laboratorio Aumentato

App interattiva per laboratori scolastici multimediali (AR, audiovisivo). Basata su scaffold `web-db-user`. L'app di riferimento per lo stile è **Shakespeare Quiz** (`/tmp/shakespeare-quiz`).

## Percorsi

- **Progetto**: `/home/user/laboratorio-visivo`
- **Preview**: https://3000-iycc2cajgdo49lj9lv8lq.sandbox.easy-peasy.ai/
- **Production**: https://laboratorio-visivo-2.easy-peasy.site

## Palette e tipografia

L'app ha un tema caldo/terroso (carta vintage). I colori personalizzati in `client/src/index.css`:

| Variabile | Valore |
|-----------|--------|
| `--plum` | `oklch(55% .115 42)` — primario per icone e accenti |
| `--gold` | `oklch(68% .1 72)` — accenti secondari |
| `--success` | `oklch(55% .12 145)` — stati positivi |
| `--primary` | `oklch(55% 0.115 42)` — sfondo bottoni (stesso di plum) |

Font: `Cambria, Georgia, "Times New Roman", serif` con `text-transform: uppercase` globale.

Tutti gli input hanno `text-align: left` e `text-transform: none` (override globale). **Nella sidebar docente** gli input vanno centrati con `!text-center` (cursore e testo partono dal centro). Fuori dalla sidebar (es. dashboard) resta `!text-left`.

## Regole di stile per l'allineamento a Shakespeare Quiz

### Bottoni

Usare **sempre** il componente shadcn `<Button>` (mai `<button>` raw) per i pulsanti primari:

```tsx
import { Button } from "@/components/ui/button";

<Button onClick={handler} disabled={condition} className="w-full h-9 text-sm font-semibold" size="sm">
  {loading ? <Loader2 className="size-4 animate-spin" /> : "TESTO"}
</Button>
```

### Regola RIAPRI: mai disabilitare per campi vuoti

Il pulsante RIAPRI **NON deve mai avere `disabled` legato alla validazione dei campi** (codice/password). La validazione avviene SOLO al click con toast di errore, come in Shakespeare Quiz:

```tsx
// ✅ CORRETTO — solo loading come condizione di disable
<Button onClick={handleReopen} disabled={reopening} className="w-full h-9 text-sm font-semibold" size="sm">
  {reopening ? <Loader2 className="size-4 animate-spin" /> : "RIAPRI"}
</Button>

// ❌ SBAGLIATO — NON condizionare il disabled ai campi vuoti
<Button onClick={handleReopen} disabled={reopening || code.length !== 4 || !password.trim()} ...>
```

Validazione al click (con toast, non silenziosa):
```tsx
const handleReopen = async () => {
  if (reopenCode.length !== 4) { toast.error("Inserisci un codice valido di 4 cifre"); return; }
  if (!reopenPassword.trim()) { toast.error("Inserisci la password della classe."); return; }
  // ... api call
};
```

Così il pulsante ha sempre hover (`hover:bg-primary/90`), colore pieno e cursore pointer — identico a CREA CLASSE.

### Input

Usare `rounded-md border bg-transparent` (NON `rounded-lg border-input bg-white font-sans`):

```tsx
// Input nella dashboard (allineati a sinistra)
<input className="w-full h-9 px-3 rounded-md border bg-transparent text-sm !text-left" />

// Input nella sidebar (centrati, cursore al centro)
<input className="w-full h-9 px-3 rounded-md border bg-transparent text-sm !text-center" />
```

Se l'input ha un'icona a sinistra: `pl-8` con icona `left-2.5`.

### Icone

- Icona principale (edificio scuola): `School` da `lucide-react`, contenitore `bg-plum/10` con `text-plum`
- Icona sezione "APRI UNA NUOVA CLASSE": `Plus` con `text-plum`
- Icona sezione "RIAPRI UNA CLASSE": `KeyRound` con `text-plum`
- Icona codice: `Hash` posizionato `left-2.5`

### Link di navigazione

I link "Area docente" / "Area studenti" usano `<a>` (NON `<button>`) con stile:

```tsx
<a href="/docente" className="inline-flex items-center gap-2 rounded-md border border-border bg-card px-3.5 py-2 text-sm font-medium text-foreground shadow-sm transition hover:border-plum/40 hover:text-plum">
  <School className="size-4" />
  Area docente
</a>
```

### Spaziatura sidebar

Usare `space-y-2` (non `space-y-2.5`) tra gli elementi della sidebar.

### Link AREA DOCENTI (Home.tsx)

Il link "Area docente" nella schermata studente deve avere `mb-4` per distanziarlo dalla card sottostante:

```tsx
<a href="/docente" className="inline-flex items-center gap-2 rounded-md border border-border bg-card px-3.5 py-2 text-sm font-medium text-foreground shadow-sm transition hover:border-plum/40 hover:text-plum mb-4">
```

### Placeholder dashboard (nessuna classe selezionata)

Il testo mostrato quando nessuna classe è selezionata:
> "Crea una nuova classe dalla barra laterale oppure riaprine una già esistente."

## Pagine chiave

### `client/src/pages/Home.tsx`
Schermata studente: titolo, link "Area docente", card con codice classe. Usa `School` da lucide-react.

### `client/src/pages/TeacherDashboard.tsx`
Dashboard docente completa con sidebar (crea/riapri classe, lista classi) e pannello principale (gestione sessione, rubric, report). È il file più grande (~1070 righe). Importa `Button` da shadcn, `Loader2` e `KeyRound` da lucide-react.

### `client/src/pages/StudentSubmit.tsx`
Invio elaborati studente per gruppo.

## Deploy

```bash
# Preview (sviluppo)
webdev_deploy project_dir="/home/user/laboratorio-visivo" mode="preview"

# Checkpoint (obbligatorio prima di production)
webdev_save_checkpoint project_dir="/home/user/laboratorio-visivo" description="..."

# Production (solo dopo conferma utente)
webdev_deploy project_dir="/home/user/laboratorio-visivo" mode="production"
```

## Rinominare l'app

Modificare in 4 file:
1. `client/index.html` — `<title>` e `<meta name="description">`
2. `client/src/pages/Home.tsx` — `<h1>`
3. `client/src/pages/TeacherDashboard.tsx` — titolo header + chiave localStorage (`lv2_active_class_id`)
4. `client/src/pages/StudentSubmit.tsx` — eventuali riferimenti

## Cornice embeddable (iframe)

L'app supporta l'embedding in iframe con auto-resize dell'altezza. Il `postMessage` è già in `client/src/App.tsx`:

```tsx
useEffect(() => {
  const send = () => {
    const h = document.documentElement.scrollHeight;
    window.parent.postMessage({ type: "labvisivo:height", height: h }, "*");
  };
  send();
  const obs = new ResizeObserver(send);
  obs.observe(document.body);
  return () => obs.disconnect();
}, []);
```

Il wrapper HTML da fornire all'utente per il blog (`embed.html` nella root del progetto):

```html
<!--LABORATORIO AUMENTATO-->
<div style="background: rgb(250, 248, 245); border-radius: 16px; box-shadow: rgba(0,0,0,0.08) 0px 4px 20px; font-family: system-ui, -apple-system, sans-serif; margin: 0px auto; max-width: 800px; overflow: hidden;">
  <div style="background: linear-gradient(135deg, rgb(210, 190, 170) 0%, rgb(230, 215, 200) 100%); padding: 16px 20px; text-align: center;">
    <span style="color: #3d2b1f; font-family: 'Cambria','Hoefler Text','Times New Roman',serif; font-size: 15px; font-weight: 600; letter-spacing: 1px;">LABORATORIO AUMENTATO</span>
  </div>
  <div style="text-align: center;">
    <iframe id="laboratorioAumentatoIframe" loading="lazy" src="https://laboratorio-visivo-2.easy-peasy.site/" style="border: none; display: block; height: 600px; min-width: 100%; transition: height 0.2s ease; width: 1px;" title="Laboratorio Aumentato"></iframe>
  </div>
</div>
<script>
(function() {
  var iframe = document.getElementById('laboratorioAumentatoIframe');
  if (!iframe) return;
  window.addEventListener('message', function(e) {
    if (e.data && e.data.type === 'labvisivo:height' && typeof e.data.height === 'number') {
      if (e.data.height > 100) iframe.style.height = e.data.height + 'px';
    }
  });
})();
</script>
```

Header: gradiente beige/marrone chiaro `rgb(210, 190, 170) → rgb(230, 215, 200)` con testo `#3d2b1f`. Messaggio postMessage: `labvisivo:height`.

## Testi personalizzabili

In `client/src/pages/StudentSubmit.tsx` le istruzioni per gli studenti sono scritte in italiano generico (senza riferimenti ad autori specifici):
- Spiegazione: NON contiene riferimenti ad autori (es. Rosalía de Castro)
- Lettura audio: "in lingua straniera" (NON "in spagnolo")

## ELIMINA CLASSE

Il pulsante ELIMINA CLASSE è nella dashboard (NON nella sidebar). Comportamento:

1. Pulsante rosso con icona `Trash2`, visibile solo quando una classe è selezionata
2. Click → `confirm()` di conferma
3. Chiama l'endpoint `classes.delete` (verifica password insegnante)
4. Cancella dal DB: classe, submission, valutazioni
5. Rimuove dalla lista sidebar e chiude immediatamente la dashboard

```tsx
// Pulsante (nella dashboard, sotto il titolo classe)
<button
  onClick={handleDeleteClass}
  disabled={deleteClassMutation.isPending}
  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md border border-red-300 bg-red-50 text-red-600 text-xs font-medium hover:bg-red-100 hover:border-red-400 transition-colors disabled:opacity-50"
>
  <Trash2 className="size-3.5" />
  ELIMINA CLASSE
</button>
```

```tsx
// Handler
const handleDeleteClass = async () => {
  if (!selectedClass) return;
  if (!confirm(`Eliminare definitivamente "${selectedClass.name}"? L'azione non è reversibile.`)) return;
  try {
    await deleteClassMutation.mutateAsync({
      classId: selectedClass.id,
      teacherPassword: selectedClass.teacherPassword,
    });
    setClasses((prev) => prev.filter((c) => c.id !== selectedClass.id));
    setSelectedClassId(null);
    setSelectedSubmission(null);
    setSubmissions([]);
    setEvaluations([]);
    toast.success("Classe eliminata.");
  } catch (e: any) {
    toast.error(e?.message || "Errore durante l'eliminazione.");
  }
};
```

Endpoint server in `server/routers.ts`:
```tsx
delete: publicProcedure
  .input(z.object({ classId: z.string(), teacherPassword: z.string() }))
  .mutation(async ({ input }) => {
    const d = requireDb();
    const [cls] = await d.select().from(schema.classes).where(eq(schema.classes.id, input.classId));
    if (!cls) throw new Error("Classe non trovata.");
    if (cls.teacherPassword !== input.teacherPassword) throw new Error("Password insegnante errata.");
    await d.delete(schema.classes).where(eq(schema.classes.id, input.classId));
    await d.delete(schema.submissions).where(eq(schema.submissions.classId, input.classId));
    await d.delete(schema.evaluations).where(eq(schema.evaluations.classId, input.classId));
    return { success: true };
  }),
```

**NB**: La sidebar NON ha più l'icona trash — la lista classi mostra solo nome e codice, cliccabili per selezione.

## Differenze rispetto a Shakespeare Quiz

- Nome app: "LABORATORIO AUMENTATO" vs "SHAKESPEARE QUIZ"
- Shakespeare Quiz è in `/tmp/shakespeare-quiz` (sola lettura, riferimento)
- Laboratorio Aumentato ha campi extra nella creazione classe: N. gruppi, Data, Titolo del progetto
- Shakespeare Quiz NON ha `KeyRound` (usa `Key` in alcune versioni)
- Entrambi condividono la stessa palette (`--plum`, `--primary`, `--gold`)
- **RIAPRI**: in SQ il pulsante non è mai disabilitato per campi vuoti — la validazione avviene al click con toast
- **Embed**: Laboratorio Aumentato supporta embedding iframe con postMessage auto-resize; SQ no
- **Testi**: Laboratorio Aumentato ha istruzioni generiche (no autore specifico, "lingua straniera"); SQ ha testi fissi su Shakespeare

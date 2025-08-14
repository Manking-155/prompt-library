# slides-prompt-techniques

Markdown-first slide system for a 10' talk + 5' Q&A about prompt writing techniques, tailored for a hospital app team in Japan (Dev, Sales, OA). No real data; synthetic examples only.

## Prerequisites
- Node.js LTS (>= 18)
- npm
- Pandoc (system install):
  - macOS: `brew install pandoc`
  - Windows: `choco install pandoc` (or download installer)
  - Linux: `apt-get install pandoc` or your distro package manager

## Install
```
npm i
```

## Run (HTML Preview)
```
npm run dev
```

Alternative:
```
npm run preview
```

## Build outputs
- Build Marp PPTX:
```
npm run build:pptx
```
- Build Marp PDF:
```
npm run build:pdf
```
- Build Pandoc PPTX (editable by Sales/OA):
```
npm run build:pandoc
```
- Build all:
```
npm run build:all
```

Outputs are written to `dist/`.

## Project structure
- `src/slides.md`: main deck (7–10 slides, speaker notes)
- `src/partials/…`: reusable content blocks (before-after, checklist)
- `themes/reference.pptx`: minimal PPTX template with logo area (used by Pandoc)
- `themes/marp.css`: lightweight Marp CSS theme (font, colors, high-contrast)
- `reveal/reveal-custom.css` & `reveal/reveal.config.json`: reveal-md config for HTML preview
- `dist/`: output folder

## Editing guidelines
- 1 idea per slide, ≤ 6 bullets
- Use 5-part structure: Role & Objective, Instructions, Examples, Context, Final steps
- Speaker notes for each slide (short, actionable)
- No real data; only synthetic placeholders and anonymized values

## Mapping for Dev/Sales/OA
- Dev: iterate on `src/slides.md` and `src/partials/*`, run `npm run dev` for preview
- Sales/OA: after `npm run build:pandoc`, edit `dist/slides.pandoc.pptx` in PowerPoint
- Keep changes in git via PRs

## Safety & compliance
- No secrets committed
- No real patient data; follow anonymization and access control principles

## Troubleshooting
- If `reveal-md` or `marp` are missing, run `npm i` to install dev dependencies.
- Ensure Pandoc is installed for `build:pandoc`.

# PR: Scaffold slides-prompt-techniques (Markdown-first deck)

## Summary
- Add Markdown-first slide system for 10' talk + 5' Q&A about prompt techniques
- Includes Marp/Pandoc build targets and Reveal preview
- Contains reusable partials (before/after, checklist, template)
- Tailored for hospital app in Japan; synthetic data only

## Changes
- Batch 1: build scripts, slides deck, partials, reveal config, marp theme, README, .gitignore, dist/.gitkeep
- Batch 2: CLAUDE_ROVO.md, 5-part template partial, reveal fragments, PR body

## How to run
```
npm i
npm run dev            # HTML preview (reveal-md)
npm run build:all      # Export PPTX/PDF (Marp) and PPTX via Pandoc
```
- Sales/OA: edit `dist/slides.pandoc.pptx` if PowerPoint tweaks are needed

## Safety
- No secrets, no real patient data, examples are synthetic
- Follow access control; CSV/JSON outputs are anonymized

## Checklist
- [x] 7–10 slides, 1 idea/slide, with speaker notes
- [x] Structured vs Unstructured before/after (2 pairs)
- [x] Japan context (hospital workflows, compliance)
- [x] Build scripts & docs

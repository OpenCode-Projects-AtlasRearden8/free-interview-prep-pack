# STATUS

## What was built

A self-contained freebie pack of interview-week printables for Asdale
Dynamics, LLC: nine fill-in-by-hand sheets that build into polished,
unbranded, print-ready PDFs with one local script. No accounts, no network
calls, no data file — nothing about the user's job hunt ever becomes
computer data, because the sheets are designed to be printed and filled out
with a pen.

The nine sheets (`templates/*.html`, shared `print.css`), each one PDF:

- `star-story-worksheet` (2 pp) — story menu + three full STAR blocks
  (Situation / Task / Action / Result) with generous writing lines and
  warm coaching notes.
- `practice-question-cards` (2 pp) — eight cut-out question cards, each with
  "why they ask it," a two-line practice space, and a kind 1–4 self-scoring
  scale (1 = rough, that's fine … 4 = ready to say in the room) plus a
  one-thing-to-tweak line.
- `company-research-sheet` (1 p) — source checklist with freshness, "what
  they do in my own words," proud-of-right-now, the problem this role
  solves, people you'll meet, and a three-box honest fit check.
- `questions-to-ask` (1 p) — grouped honest questions (work / team /
  success / practical) plus write-your-own lines.
- `outfit-bag-checklist` (1 p) — night-before outfit and bag columns with
  drawn (CSS, not font) checkboxes.
- `day-of-timeline` (1 p) — night-before-through-thank-you table with
  pencil-in times, a calm lateness script, and done-checkboxes.
- `reflection-log` (1 p) — one-kind-pass debrief: gut check, what went
  better, what was harder, surprised-me questions, their vocabulary,
  thank-you-sent tracking.
- `thank-you-note-email` (1 p) — subject-line picks and a four-sentence
  copy-change-send draft with anti-robot rules.
- `thank-you-note-paper` (1 p) — a paper-note block with the two-minute
  version to hand-copy, plus a mail-day checklist.

Layout of the pack:

- `build.py` — the one build script. Renders each static HTML template to
  PDF via locally installed WeasyPrint. Flags: `--sheets`, `--out`,
  `--keep-html` (browser "Print to PDF" route), `--list`. Missing templates
  and unknown sheet names fail with plain-English messages, not stack
  traces.
- `templates/` — the nine HTML sources plus one shared `print.css`
  (letter-size @page, calm teal accent, CSS-drawn checkboxes so no font
  dependency, grayscale-safe palette, unbranded).
- `printables/` — the nine rebuilt sample PDFs.
- `docs/how-to-use.md` — sheet-by-sheet plain-English usage guide with
  timing suggestions across interview week.
- `tests/test_build.py` — 66 tests (below).
- `README.md` — quick start, usage, how all nine sheets fit together, and
  the no-data notice; credits Asdale Dynamics, LLC.
- `LICENSE` (MIT, "Copyright (c) 2026 Asdale Dynamics, LLC"),
  `requirements.txt`, `pytest.ini`, `.gitignore`.

## How to run it

```bash
python3 -m venv .venv && source .venv/bin/activate   # once
pip install -r requirements.txt                      # once
python3 build.py                                     # build all 9 PDFs
pytest -q                                            # run the test suite
```

Optional: `--keep-html` (browser-printable copies in `printables/html/`),
`--sheets <comma-separated names>`, `--out <folder>`, `--list`.

## Verification results

- All nine templates build; page counts are exactly as designed and
  verified by pypdf (2, 2, 1, 1, 1, 1, 1, 1, 1 = 11 pages total), and
  checked visually as rendered page images (pdftoppm at 40 DPI) — no
  stranded single-line pages, no content split mid-block; `page-break-inside:
  avoid` guards every story block, question card, and section.
- `pytest -q`: **66 passed**. Coverage includes: all nine sheets listed and
  present; templates complete (doctype, stylesheet link, title, closing
  tag) and static (no template tokens ever sneak in); every PDF starts with
  `%PDF`, ends with `%%EOF`, is substantial (>5 KB), exactly US Letter
  (612×792 pt), has the expected page count, has a real selectable text
  layer (>200 chars, signature phrase per sheet), and stays unbranded (no
  "Asdale", no URLs); the CLI builds all nine end-to-end via subprocess,
  builds a single sheet subset, `--list` works, an unknown sheet name exits
  2 with a plain-English message and no traceback; a missing template file
  raises the friendly error; `--keep-html` copies point at the stylesheet
  from their new location; no secret-shaped strings (API keys, tokens,
  private key blocks, password=) and no personal-data-shaped strings (US
  phone patterns, emails) anywhere in repo text files; LICENSE holds the
  exact copyright line; README credits the LLC and documents build + tests.
- `--list`, `--sheets` filtering, and `--keep-html` exercised both by tests
  and by hand during development.

## Known gaps

- The sheets are fill-by-hand only: there is intentionally no JSON/data
  route (keeps the repo free of personal data by construction). A
  data-filled variant would need a separate mechanism if ever wanted.
- Exact page counts are asserted in tests, so adding content to any sheet
  requires re-checking pagination by hand — deliberate, but it means
  trivial content edits can turn into a test re-baseline.
- Fonts follow named stacks (Helvetica/Arial with Noto/DejaVu fallbacks);
  checkbox shapes are CSS-drawn precisely so missing fonts can't break
  them, but overall look varies slightly on machines without those fonts.
- Windows untested (development machine is Linux); venv commands differ
  slightly there and the README covers Unix-style shells.
- The reflection log's gut-check circles are filled in by circling with a
  pen (by design there are no interactive form fields; WeasyPrint does not
  emit fillable AcroForm fields).
- Card cutting guides are dashed card borders, not bleed-aware crop marks;
  scissors-only use is assumed, fine at home-print scale.

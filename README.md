# Free Interview Prep Pack

Interview week, one printable at a time — nine calm, fill-in sheets that build
into polished PDFs on your own computer. No accounts, no uploads, no "free"
site that quietly asks for your resume first.

Everything here is meant to be **printed and filled out with a pen** — the
pages have real writing room, short prompts, and half as much advice as you
probably feared. They work just as well for a first-ever interview as for a
tenth-year nurse changing jobs.

The nine sheets, in the order you'll use them:

| Sheet | What it's for | Pages |
|---|---|---|
| `star-story-worksheet` | Turn real experiences into ready "tell me about a time" stories | 2 |
| `practice-question-cards` | Cut-out cards for practicing out loud, with kind self-scoring (1 rough → 4 ready) | 2 |
| `company-research-sheet` | Twenty focused minutes of company homework, in your own words | 1 |
| `questions-to-ask` | Honest questions *you* should ask — you're deciding too | 1 |
| `outfit-bag-checklist` | What to wear, what to carry, decided the night before | 1 |
| `day-of-timeline` | Hour-by-hour companionship from the night before to the thank-you sent | 1 |
| `reflection-log` | The gentle after-interview debrief — once, kindly, then done | 1 |
| `thank-you-note-email` | A short email draft that sounds like you, not a template | 1 |
| `thank-you-note-paper` | A handwritten note, mailed while it still matters | 1 |

Built by **Asdale Dynamics, LLC** (Dylan Asdale) as part of our plain-English
toolkit: AI and job-hunting explained like a friend would — step by step,
never condescending. The STAR worksheet and question cards pair naturally
with our free resume pack and the mock-interview coach webapp.

## Quick start (plain English, one time)

You need Python 3.10 or newer, installed once, on your computer. Get it from
python.org — or check whether you have it already:

```bash
python3 --version
```

Then, from inside this folder, in a terminal:

```bash
# 1. Make a private workspace for the tools (called a "virtual environment"):
python3 -m venv .venv

# 2. Turn it on:
source .venv/bin/activate

# 3. Install the small tools this pack needs:
pip install -r requirements.txt
```

That's setup. It stays done.

## Using it (the easy part)

```bash
python3 build.py
```

Nine PDFs appear in `printables/`. Print at 100% on US Letter paper — the
sheets are drawn for it. Fill them out with a pen; a pencil works even better
for the first pass, because rough drafts are the whole technique.

Useful variants:

```bash
python3 build.py --list                                  # see every sheet
python3 build.py --sheets questions-to-ask,day-of-timeline   # build only some
python3 build.py --out ~/Desktop/interview-week          # put them elsewhere
python3 build.py --keep-html                             # also save browser-printable HTML
```

With `--keep-html`, each PDF gets a matching file in `printables/html/` that
you can open in a browser and choose "Print to PDF" yourself — an extra path
for computers where the first route won't cooperate. Keep the folders
together so the HTML can find its stylesheet.

Prefer no commands at all? Every sheet in `templates/` is a plain HTML page
that prints nicely from a browser too.

## The tests (so you can trust the pack)

```bash
pytest -q
```

Sixty-six checks run automatically. Every sheet must build to a real,
openable US-Letter PDF with a selectable text layer; the page counts must
match what the designs promise; the printables must stay completely
unbranded; the command line must work end to end and fail *nicely* (plain
English, no stack trace) when a sheet name is mistyped or a template goes
missing; and the repository must stay free of both secrets and real-looking
personal data. The tests keep the pack honest whenever anyone changes it.

## How to use the sheets (the friendly tour)

Print the whole pack at once and keep it in one folder — or spread over the
week like this:

1. **A quiet evening (20 min):** pick your three stories on the STAR
   worksheet and draft just one of them. Messy handwriting is correct.
2. **The next evening (20 min):** cut the practice cards and do two out
   loud. Score with the kind scale — a "1" just means tomorrow's homework.
3. **Midweek (20 min):** company research sheet. Stop while it's still
   interesting.
4. **The night before:** outfit and bag checklist, day-of timeline, then
   good sleep on purpose.
5. **Interview day:** follow the timeline page more than your nerves.
6. **That evening:** thank-you note, reflection log once, done.

## A note about your info

There is no data file here — nothing about you is stored, typed, or
transmitted anywhere. The sheets ask you to write with a pen for exactly
that reason. Keep finished, filled-in pages somewhere physical or private;
the internet doesn't need your interview notes.

## License

MIT — free to use, change, and share, including for anything you run or
publish. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.

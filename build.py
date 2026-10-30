#!/usr/bin/env python3
"""
Free Interview Prep Pack build script.

One script, all local, no accounts:

  build:      python3 build.py
  look in:    printables/          (nine polished PDFs)

The templates are fill-in printables: you print them and fill them out with
a pen (or open a template in a browser and print it yourself). They are
static by design, so nothing about your job hunt ever becomes data on this
computer.

Optional flags:

  --sheets star-story-worksheet,practice-question-cards   build only some sheets
  --out PATH            write the PDFs somewhere else
  --list                show every available sheet and stop

Sheets (templates/), matched to the README:

  star-story-worksheet   STAR stories, planned kindly
  practice-question-cards   cut-out cards with kind self-scoring
  company-research-sheet    what to learn about them, in one page
  questions-to-ask       the questions *you* should ask
  outfit-bag-checklist   what to wear and what to carry
  day-of-timeline        hour by hour, night before to thank-you sent
  reflection-log         the gentle after-interview debrief
  thank-you-note-email   an email draft that sounds like you
  thank-you-note-paper   a handwritten note, promptly mailed

Tests use the same functions this script calls: see tests/test_build.py.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATES_DIR = ROOT / "templates"
DEFAULT_OUT = ROOT / "printables"

SHEETS = [
    "star-story-worksheet",
    "practice-question-cards",
    "company-research-sheet",
    "questions-to-ask",
    "outfit-bag-checklist",
    "day-of-timeline",
    "reflection-log",
    "thank-you-note-email",
    "thank-you-note-paper",
]

STYLESHEET = "print.css"


class BuildError(Exception):
    """A plain-English message shown to the user, instead of a stack trace."""


def template_path(sheet: str) -> Path:
    return TEMPLATES_DIR / f"{sheet}.html"


def available_list() -> str:
    return "\n".join(f"  - {s}.html" for s in SHEETS)


def read_template(sheet: str) -> Path:
    """Return the template path for a sheet, or raise a friendly error."""
    path = template_path(sheet)
    if not path.exists():
        raise BuildError(
            f"Couldn't find the template: {path}\n"
            f"Available templates:\n{available_list()}"
        )
    return path


def render_html_text(sheet: str) -> str:
    """Return the raw HTML text of a sheet template (for the browser route)."""
    template_path = read_template(sheet)
    text = template_path.read_text(encoding="utf-8")
    if STYLESHEET not in text:
        raise BuildError(
            f"{sheet}.html should link its stylesheet "
            f"({STYLESHEET}) but the link is missing."
        )
    return text


def import_weasyprint():
    try:
        from weasyprint import HTML
        return HTML
    except ModuleNotFoundError:
        python_name = Path(sys.executable).name
        raise BuildError(
            "WeasyPrint isn't installed yet. It's the tool that turns the "
            "HTML templates into PDFs.\n"
            f"Install it with:  {python_name} -m pip install -r requirements.txt\n"
            "(run that from this folder; the README walks through it in plain English)"
        )


def page_count(pdf_path: Path):
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(pdf_path)).pages)
    except ModuleNotFoundError:
        return None


def render_pdf(sheet: str, out_path: Path) -> None:
    """Turn one sheet's HTML into a PDF, with the stylesheet found locally."""
    HTML = import_weasyprint()
    html_text = render_html_text(sheet)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(
        string=html_text,
        base_url=str(TEMPLATES_DIR),
    ).write_pdf(target=str(out_path))


def build_sheet(sheet: str, out_dir: Path, keep_html: bool = False) -> Path:
    out_path = out_dir / f"{sheet}.pdf"
    render_pdf(sheet, out_path)

    if keep_html:
        # The stylesheet lives next to the templates, so a copy placed in
        # printables/html/ has to point up two folders to find it. That's why
        # the HTML route asks you to keep the folders together.
        html_for_browser(out_path.parent, sheet)
    return out_path


def html_for_browser(out_dir: Path, sheet: str) -> Path:
    """Save a browser-printable copy of a sheet under out_dir/html/."""
    text = render_html_text(sheet)
    text = text.replace(f'href="{STYLESHEET}"', f'href="../../templates/{STYLESHEET}"', 1)
    out_path = out_dir / "html" / f"{sheet}.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    return out_path


def build_all(
    sheets: list,
    out_dir: Path = DEFAULT_OUT,
    keep_html: bool = False,
) -> list:
    """Build every requested sheet; print friendly progress; return PDF paths."""
    pdf_paths: list = []
    total = len(sheets)
    print(f"Building {total} PDF{'s' if total != 1 else ''} into {out_dir}")

    for sheet in sheets:
        out_path = build_sheet(sheet, out_dir, keep_html=keep_html)
        pdf_paths.append(out_path)
        pages = page_count(out_path)
        size_kb = out_path.stat().st_size // 1024
        pages_text = f"{pages} page{'s' if pages != 1 else ''}, " if pages is not None else ""
        print(f"  [ok] {out_path.name}  ({pages_text}{size_kb} KB)")
    return pdf_paths


def show_list() -> None:
    print("Sheets (each builds one PDF in printables/):")
    for sheet in SHEETS:
        print(f"  {sheet}.html")
    print(f"\nOutput folder: {DEFAULT_OUT}")


def parse_list_arg(text: str, choices: list, flag: str) -> list:
    items = [item.strip() for item in text.split(",") if item.strip()]
    if not items:
        raise argparse.ArgumentTypeError(
            f"{flag} needs names like: {','.join(choices)}"
        )
    for item in items:
        if item not in choices:
            raise argparse.ArgumentTypeError(
                f"unknown {flag} name '{item}'. Choices: {', '.join(choices)}"
            )
    return items


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the interview prep pack PDFs (local, no accounts).",
        epilog="Examples:  python3 build.py\n"
        "           python3 build.py --sheets star-story-worksheet",
    )
    parser.add_argument(
        "--sheets", default=",".join(SHEETS),
        help="comma-separated sheets (default: all nine)",
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="output folder")
    parser.add_argument(
        "--keep-html", action="store_true",
        help="also save browser-printable HTML copies (for 'Print to PDF')",
    )
    parser.add_argument("--list", action="store_true", help="show the sheets and stop")
    args = parser.parse_args(argv)

    if args.list:
        show_list()
        return 0

    try:
        sheets = parse_list_arg(args.sheets, SHEETS, "--sheets")
        build_all(sheets, out_dir=args.out, keep_html=args.keep_html)
    except argparse.ArgumentTypeError as err:
        print(f"Build didn't start: {err}", file=sys.stderr)
        return 2
    except BuildError as err:
        print(f"Build stopped: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

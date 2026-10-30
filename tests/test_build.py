"""
Tests for the Free Interview Prep Pack.

The promise this pack makes is that every sheet builds into a real,
readable, unbranded PDF with one local command. So every test here guards
one part of that promise:

  - every template exists and is complete HTML wired to the stylesheet
  - every sheet builds a valid, openable PDF with selectable text
  - the output stays unbranded (no company names in the printables)
  - the page counts stay as designed (nothing spills onto a surprise page)
  - the command line works end-to-end and fails with plain-English errors
  - the repo contains no secrets and no real-looking personal data
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import build as pack

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"
REPO_TEXT_SUFFIXES = (".py", ".md", ".txt", ".html", ".css", ".json", ".ini", ".cfg")

# The exact page count each sheet is designed for. If a worksheet ever
# overflows to a new page, that's a visible design change — these tests make
# it show up as a test failure instead of a surprise for the user.
EXPECTED_PAGES = {
    "star-story-worksheet": 2,
    "practice-question-cards": 2,
    "company-research-sheet": 1,
    "questions-to-ask": 1,
    "outfit-bag-checklist": 1,
    "day-of-timeline": 1,
    "reflection-log": 1,
    "thank-you-note-email": 1,
    "thank-you-note-paper": 1,
}

# One phrase per sheet that should land in the extracted text layer.
MARKERS = {
    "star-story-worksheet": "what did you actually do",
    "practice-question-cards": "tell me about yourself",
    "company-research-sheet": "company research sheet",
    "questions-to-ask": "questions you should ask",
    "outfit-bag-checklist": "the bag",
    "day-of-timeline": "day-of timeline",
    "reflection-log": "post-interview reflection log",
    "thank-you-note-email": "copy, change the brackets, send",
    "thank-you-note-paper": "mail-day checklist",
}


@pytest.fixture(scope="module")
def built(tmp_path_factory) -> list:
    """Build every sheet once for the module; return the PDF paths."""
    out = tmp_path_factory.mktemp("printables")
    return pack.build_all(list(pack.SHEETS), out_dir=out)


def pdf_pages(pdf_path: Path) -> int:
    from pypdf import PdfReader
    return len(PdfReader(str(pdf_path)).pages)


def pdf_text(pdf_path: Path) -> str:
    """Extracted text, lower-cased, all whitespace collapsed for matching."""
    from pypdf import PdfReader
    raw = "\n".join(page.extract_text() or "" for page in PdfReader(str(pdf_path)).pages)
    return re.sub(r"\s+", " ", raw).lower()


# -------- templates: complete and wired up --------


def test_every_sheet_is_listed_in_build_script():
    """The nine sheets the pack promises must all be in build.py's list."""
    assert sorted(pack.SHEETS) == sorted(EXPECTED_PAGES.keys())


@pytest.mark.parametrize("sheet", list(pack.SHEETS))
def test_template_exists(sheet):
    assert pack.template_path(sheet).is_file()


@pytest.mark.parametrize("sheet", list(pack.SHEETS))
def test_template_is_complete_html(sheet):
    text = pack.template_path(sheet).read_text(encoding="utf-8")
    assert text.lstrip().lower().startswith("<!doctype html")
    assert 'href="print.css"' in text  # every sheet wears the shared stylesheet
    assert "</html>" in text
    assert "<title>" in text


@pytest.mark.parametrize("sheet", list(pack.SHEETS))
def test_templates_stay_static(sheet):
    """Sheets are fill-by-hand printables: no template tokens ever sneak in."""
    assert "{{" not in pack.template_path(sheet).read_text(encoding="utf-8")


# -------- building: every sheet makes a real PDF --------


def test_build_all_returns_every_file(built):
    names = sorted(path.name for path in built)
    assert names == sorted(f"{sheet}.pdf" for sheet in pack.SHEETS)


@pytest.mark.parametrize("sheet", list(pack.SHEETS))
def test_pdf_is_valid_and_read_openable(built, sheet):
    target = next(p for p in built if p.name == f"{sheet}.pdf")
    data = target.read_bytes()
    assert data.startswith(b"%PDF"), f"{target.name} doesn't start with a %PDF header"
    assert b"%%EOF" in data[-1024:], f"{target.name} has no EOF marker"
    assert len(data) > 5_000, f"{target.name} looks suspiciously empty"

    from pypdf import PdfReader
    reader = PdfReader(str(target))
    assert len(reader.pages) == EXPECTED_PAGES[sheet]
    page = reader.pages[0]
    # US Letter, per the @page rule — keeps the print dialog honest.
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    assert abs(width - 612) < 2 and abs(height - 792) < 2


@pytest.mark.parametrize("sheet", list(pack.SHEETS))
def test_pdf_has_real_text_layer(built, sheet):
    target = next(p for p in built if p.name == f"{sheet}.pdf")
    text = pdf_text(target)
    assert len(text) > 200, f"{target.name} has almost no selectable text"
    assert MARKERS[sheet] in text, f"{target.name} lost its signature content"


@pytest.mark.parametrize("sheet", list(pack.SHEETS))
def test_pdfs_stay_unbranded(built, sheet):
    """Unbranded is the point: nothing in the printables names the maker."""
    target = next(p for p in built if p.name == f"{sheet}.pdf")
    text = pdf_text(target)
    for banned in ("asdale", "dylanasdale", "github.io", "dynamic"):
        assert banned not in text, f"{target.name} mentions '{banned}' — keep it unbranded"


# -------- the command line, end to end --------


def test_cli_builds_everything(tmp_path):
    result = subprocess.run(
        [sys.executable, "build.py", "--out", str(tmp_path / "out")],
        cwd=ROOT, capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, result.stderr
    built = sorted((tmp_path / "out").glob("*.pdf"))
    assert len(built) == len(pack.SHEETS)
    assert "Building 9 PDFs" in result.stdout


def test_cli_builds_one_sheet(tmp_path):
    result = subprocess.run(
        [sys.executable, "build.py", "--sheets", "day-of-timeline",
         "--out", str(tmp_path / "one")],
        cwd=ROOT, capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, result.stderr
    assert sorted(p.name for p in (tmp_path / "one").glob("*.pdf")) == ["day-of-timeline.pdf"]


def test_cli_list_flag():
    result = subprocess.run(
        [sys.executable, "build.py", "--list"],
        cwd=ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0
    assert "star-story-worksheet.html" in result.stdout


def test_cli_unknown_sheet_fails_friendly(tmp_path):
    result = subprocess.run(
        [sys.executable, "build.py", "--sheets", "vibes-only", "--out", str(tmp_path)],
        cwd=ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 2
    assert "unknown --sheets name 'vibes-only'" in result.stderr
    assert "Traceback" not in result.stderr


def test_missing_template_raises_friendly_error(tmp_path):
    real = pack.template_path("reflection-log")
    backup = real.with_suffix(".html.bak")
    shutil.move(real, backup)
    try:
        with pytest.raises(pack.BuildError) as err:
            pack.build_sheet("reflection-log", tmp_path)
        assert "Couldn't find the template" in str(err.value)
        assert "Traceback" not in str(err.value)
    finally:
        shutil.move(backup, real)


def test_keep_html_writes_browser_copies(tmp_path):
    pack.build_sheet("questions-to-ask", tmp_path, keep_html=True)
    html_copy = tmp_path / "html" / "questions-to-ask.html"
    assert html_copy.is_file()
    text = html_copy.read_text(encoding="utf-8")
    # The copy must still find the stylesheet from its new home.
    assert 'href="../../templates/print.css"' in text


# -------- repo hygiene: no secrets, no personal data --------


def _repo_text_files():
    skip_dirs = (".git", ".venv", "__pycache__", ".pytest_cache")
    for path in ROOT.rglob("*"):
        if path.is_file() and not any(part in path.parts for part in skip_dirs):
            if path.suffix.lower() in REPO_TEXT_SUFFIXES:
                yield path


def test_repo_has_no_secret_shaped_strings():
    patterns = (
        re.compile(r"(sk-[a-zA-Z0-9]{8,})"),                # API keys
        re.compile(r"(ghp_[A-Za-z0-9]{10,})"),               # GitHub tokens
        re.compile(r"(-----BEGIN [A-Z ]*PRIVATE KEY-----)"), # key blocks
        re.compile(r"(?i)(api[_-]?key\s*[:=]\s*['\"][^'\"]{8,})"),
        re.compile(r"(?i)(password\s*[:=]\s*['\"][^'\"]{8,})"),
    )
    for path in _repo_text_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in patterns:
            assert not pattern.search(text), f"{path.name} contains a secret-shaped string"


def test_repo_has_no_real_looking_personal_data():
    """The pack ships only blanks: no phone numbers, no emails of anyone."""
    patterns = (
        re.compile(r"\b\d{3}-\d{3}-\d{4}\b"),                          # US phones
        re.compile(r"\b[\w.+-]+@[\w-]+\.[a-z]{2,}\b", re.IGNORECASE),  # emails
    )
    for path in _repo_text_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in patterns:
            assert not pattern.search(text), f"{path.name} contains personal-data-shaped text"


# -------- the legal/readme promise --------


def test_license_has_exact_copyright_line():
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "Copyright (c) 2026 Asdale Dynamics, LLC" in license_text


def test_readme_credits_and_explains():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Asdale Dynamics, LLC" in readme
    assert "build.py" in readme
    assert "pytest" in readme

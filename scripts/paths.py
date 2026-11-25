"""Shared paths. Everything is relative to the repo root."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources"            # downloaded by scripts/fetch_sources.sh (git-ignored)
TOCFL = SOURCES / "tocfl"             # github.com/ivankra/tocfl
HSK = SOURCES / "complete-hsk-vocabulary" / "wordlists" / "exclusive" / "new"
STROKES_SRC = SOURCES / "hanzi-writer-data" / "package"
CONTENT = ROOT / "content"            # hand-written stories (essays.txt)
BUILD = ROOT / "build"                # intermediate files (git-ignored)
PUBLIC = ROOT / "public"              # the website: deploy this folder
for p in (BUILD, PUBLIC / "data", PUBLIC / "strokes"):
    p.mkdir(parents=True, exist_ok=True)

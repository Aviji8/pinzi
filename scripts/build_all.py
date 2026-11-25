"""Run the whole pipeline: python scripts/build_all.py  (add --fetch to download sources first)."""
import subprocess, sys, os
from pathlib import Path
HERE = Path(__file__).resolve().parent
steps = ["step1_band_a_cards.py", "step2_band_a_stories.py", "step3_build_decks.py", "step4_build_themes.py"]
if "--fetch" in sys.argv:
    steps.insert(0, "fetch_sources.py")
env = dict(os.environ, PYTHONUTF8="1")   # UTF-8 everywhere (Windows-safe)
for s in steps:
    print(f"\n=== {s} ===")
    subprocess.run([sys.executable, "-X", "utf8", str(HERE / s)], cwd=HERE, env=env, check=True)
print("\nDone. Open public/index.html through a local server:  python -m http.server -d public 8000")

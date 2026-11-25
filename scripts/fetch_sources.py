"""Download the open word lists and stroke data into sources/ (needs git and npm)."""
import subprocess, shutil, tarfile, glob
from paths import SOURCES
SOURCES.mkdir(exist_ok=True)

def clone(url, name):
    dest = SOURCES / name
    if dest.exists():
        print("already have", name); return
    subprocess.run(["git", "clone", "--depth", "1", url, str(dest)], check=True)

clone("https://github.com/ivankra/tocfl", "tocfl")                                  # TOCFL official lists (CSV)
clone("https://github.com/drkameleon/complete-hsk-vocabulary", "complete-hsk-vocabulary")  # HSK 3.0 lists

hw = SOURCES / "hanzi-writer-data"
if not hw.exists():
    hw.mkdir()
    subprocess.run(["npm", "pack", "hanzi-writer-data@2.0.1"], cwd=hw, check=True, shell=shutil.which("npm") is None)
    with tarfile.open(glob.glob(str(hw / "*.tgz"))[0]) as t:
        t.extractall(hw, filter="data") if hasattr(tarfile, "data_filter") else t.extractall(hw)
print("Sources ready in", SOURCES)

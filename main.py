# main.py — entrypoint for make.fun news-image-20261125.
#
# Standard library only: the grading container installs nothing, so
# this program does the simplest thing the competition rules allow —
# it copies the image the repository holds (entry.png, drawn by
# generate.py) to /output/entry.png. The copy is byte-identical on
# every run: no network, no clock, no randomness.
#
#   python3 main.py            # writes /output/entry.png
#   MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "entry.png"
    shutil.copyfile(HERE / "entry.png", out)
    os.chmod(out, 0o644)
    return out


if __name__ == "__main__":
    path = main()
    print(f"wrote {path} ({path.stat().st_size} bytes)")

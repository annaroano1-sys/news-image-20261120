"""Entrypoint for the news-image-20261120 bounty (round 2).

Copies the pre-rendered entry.png next to this file to the output
directory (MAKEFUN_OUTPUT_DIR, default /output). Stdlib only.
"""
import hashlib
import os
import shutil


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    # Round 2: same contract as round 1 — one PNG, byte-identical copy.
    shutil.copyfile(src, dst)
    # Fail loudly if the copy is not byte-identical to the source.
    if _sha256(src) != _sha256(dst):
        raise RuntimeError("entry.png copy failed integrity check")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Unpack a .docx file to a directory for XML editing."""
import sys, zipfile, shutil, os

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input.docx outdir/")
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst, exist_ok=True)
    with zipfile.ZipFile(src) as z:
        z.extractall(dst)
    print(f"Unpacked: {src} → {dst}")

if __name__ == '__main__':
    main()

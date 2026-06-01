#!/usr/bin/env python3
"""Re-pack an unpacked DOCX directory back into a .docx file.

Usage:
    pack.py srcdir/ output.docx [--original original.docx]

The --original flag is accepted for interface compatibility but unused —
all content comes from srcdir.
"""
import sys, zipfile, os, argparse

def main():
    parser = argparse.ArgumentParser(description='Pack a DOCX directory into a .docx file.')
    parser.add_argument('srcdir', help='Unpacked DOCX directory')
    parser.add_argument('output', help='Output .docx path')
    parser.add_argument('--original', help='Original .docx (unused — for interface compat)')
    args = parser.parse_args()

    srcdir = os.path.abspath(args.srcdir)
    output = os.path.abspath(args.output)
    tmp = output + '.tmp'

    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for root, dirs, files in os.walk(srcdir):
            for fname in files:
                filepath = os.path.join(root, fname)
                arcname = os.path.relpath(filepath, srcdir).replace(os.sep, '/')
                zout.write(filepath, arcname)

    os.replace(tmp, output)
    print(f"Packed: {srcdir} → {output}")

if __name__ == '__main__':
    main()

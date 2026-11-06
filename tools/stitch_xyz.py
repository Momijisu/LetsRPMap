#!/usr/bin/env python3
"""Stitch one zoom level of an ordinary web-map tile set ({z}/{x}/{y}.png) into a
single picture, to feed into cut_tiles.py.

    python3 stitch_xyz.py tiles/ 5 map.png

Pick the most detailed zoom level that still fits in memory (e.g. 32 x 32 tiles
of 256 px = an 8192 px picture). Missing tiles are left transparent.
Needs Pillow: pip install pillow
"""
import os, sys
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
root, z, out = sys.argv[1], sys.argv[2], sys.argv[3]
zdir = os.path.join(root, z)
xs = sorted(int(x) for x in os.listdir(zdir) if x.lstrip('-').isdigit())
ys = sorted({int(os.path.splitext(f)[0]) for x in xs for f in os.listdir(os.path.join(zdir, str(x)))})
first = next(f for f in os.listdir(os.path.join(zdir, str(xs[0]))))
ext = os.path.splitext(first)[1]
size = Image.open(os.path.join(zdir, str(xs[0]), first)).size[0]
img = Image.new('RGBA', ((xs[-1] - xs[0] + 1) * size, (ys[-1] - ys[0] + 1) * size), (0, 0, 0, 0))
for x in xs:
    for y in ys:
        p = os.path.join(zdir, str(x), f'{y}{ext}')
        if os.path.exists(p):
            img.paste(Image.open(p).convert('RGBA'), ((x - xs[0]) * size, (y - ys[0]) * size))
img.save(out)
print(f'{out}: {img.size[0]}x{img.size[1]} px from x {xs[0]}..{xs[-1]}, y {ys[0]}..{ys[-1]} ({size} px tiles)')

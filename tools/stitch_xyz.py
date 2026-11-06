#!/usr/bin/env python3
"""Stitch one zoom level of an ordinary web-map tile set into a single picture,
to feed into cut_tiles.py.

Tile sets come in two common layouts; say which with --pattern:
  folders (default)   {z}/{x}/{y}.png
  flat files          e.g. --pattern "{z}_{x}_{y}.jpg" for files like 7_71_88.jpg

    python3 stitch_xyz.py tiles/ 5 map.png
    python3 stitch_xyz.py tiles/ 4 map.png --pattern "{z}_{x}_{y}.jpg"

Pick the most detailed zoom that still fits in memory (32 x 32 tiles of 256 px
makes an 8192 px picture). Missing tiles are left transparent.
Needs Pillow: pip install pillow
"""
import argparse, os, re
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def find_tiles(root, z, pattern):
    """Return {(x, y): path} for zoom z."""
    tiles = {}
    if pattern is None:
        zdir = os.path.join(root, str(z))
        for x in os.listdir(zdir):
            if not x.lstrip('-').isdigit():
                continue
            for f in os.listdir(os.path.join(zdir, x)):
                stem = os.path.splitext(f)[0]
                if stem.lstrip('-').isdigit():
                    tiles[(int(x), int(stem))] = os.path.join(zdir, x, f)
        return tiles
    # Turn e.g. "{z}_{x}_{y}.jpg" into a regular expression
    rx = re.escape(pattern)
    for key in ('z', 'x', 'y'):
        rx = rx.replace(re.escape('{' + key + '}'), f'(?P<{key}>-?\\d+)')
    rx = re.compile('^' + rx + '$')
    for dirpath, _, files in os.walk(root):
        for f in files:
            m = rx.match(f)
            if m and int(m.group('z')) == z:
                tiles[(int(m.group('x')), int(m.group('y')))] = os.path.join(dirpath, f)
    return tiles


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('root'); a.add_argument('zoom', type=int); a.add_argument('out')
    a.add_argument('--pattern', help='file name pattern for flat tile sets, e.g. "{z}_{x}_{y}.jpg"')
    o = a.parse_args()
    tiles = find_tiles(o.root, o.zoom, o.pattern)
    if not tiles:
        raise SystemExit(f'no tiles found for zoom {o.zoom}')
    xs = [x for x, _ in tiles]; ys = [y for _, y in tiles]
    size = Image.open(next(iter(tiles.values()))).size[0]
    img = Image.new('RGBA', ((max(xs) - min(xs) + 1) * size, (max(ys) - min(ys) + 1) * size), (0, 0, 0, 0))
    for (x, y), p in tiles.items():
        img.paste(Image.open(p).convert('RGBA'), ((x - min(xs)) * size, (y - min(ys)) * size))
    img.save(o.out)
    print(f'{o.out}: {img.size[0]}x{img.size[1]} px from {len(tiles)} tiles, '
          f'x {min(xs)}..{max(xs)}, y {min(ys)}..{max(ys)} ({size} px tiles)')


if __name__ == '__main__':
    main()

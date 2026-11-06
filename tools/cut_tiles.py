#!/usr/bin/env python3
"""Cut one big map picture into tiles for the Let's RP map.

The map works in GTA world coordinates: one map unit is one metre, x runs east
and y runs north, exactly like in-game coordinates. At zoom z a tile is 256 px
and covers 256 / 2**z metres. Tiles are saved as

    OUT/{mapID}/{z}/{plane}_{x}_{y}.png

which is what the extension asks for with tileURLFormat
"{mapID}/{z}/{p}_{x}_{-y}.png".

You need the GTA coordinates of the picture's edges. Find them once by lining up
two or three known places (see README). Example, for an 8192 x 8192 picture:

    python3 cut_tiles.py map.png out --left -5600 --right 6400 --bottom -4100 --top 7900 \\
        --zooms -3 -2 -1 0 1 2 3 --map-id 0 --name "Los Santos"

Writes out/basemaps.json too (add more maps to it by hand, or with --append).
Needs Pillow: pip install pillow
"""
import argparse, json, math, os
from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument('image'); a.add_argument('out')
    a.add_argument('--left', type=float, required=True, help='GTA x of the picture\'s left edge')
    a.add_argument('--right', type=float, required=True, help='GTA x of the right edge')
    a.add_argument('--bottom', type=float, required=True, help='GTA y of the bottom edge')
    a.add_argument('--top', type=float, required=True, help='GTA y of the top edge')
    a.add_argument('--zooms', type=int, nargs='+', default=[-3, -2, -1, 0, 1, 2])
    a.add_argument('--map-id', type=int, default=0)
    a.add_argument('--plane', type=int, default=0)
    a.add_argument('--name', default='Los Santos')
    a.add_argument('--format', default='png', choices=['png', 'jpg', 'webp'])
    a.add_argument('--append', action='store_true', help='add to an existing basemaps.json')
    o = a.parse_args()

    src = Image.open(o.image).convert('RGBA')
    W, H = src.size
    width_m, height_m = o.right - o.left, o.top - o.bottom
    print(f'{W}x{H} px over {width_m:g} x {height_m:g} m = {W / width_m:.3f} px per metre')

    for z in sorted(o.zooms):
        s = 2 ** z                      # pixels per metre at this zoom
        T = 256 / s                     # metres per tile
        scaled = src.resize((max(1, round(width_m * s)), max(1, round(height_m * s))), Image.LANCZOS)
        folder = os.path.join(o.out, str(o.map_id), str(z)); os.makedirs(folder, exist_ok=True)
        count = 0
        for i in range(math.floor(o.left / T), math.ceil(o.right / T)):
            for j in range(math.floor(o.bottom / T), math.ceil(o.top / T)):
                # tile (i, j) covers x i*T..(i+1)*T and y j*T..(j+1)*T; its top edge is y=(j+1)*T
                left_px = round((i * T - o.left) * s)
                top_px = round((o.top - (j + 1) * T) * s)
                tile = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
                tile.paste(scaled.crop((left_px, top_px, left_px + 256, top_px + 256)), (0, 0))
                if tile.getbbox() is None:
                    continue            # fully outside the picture: skip
                name = os.path.join(folder, f'{o.plane}_{i}_{j}.{o.format}')
                (tile.convert('RGB') if o.format == 'jpg' else tile).save(name)
                count += 1
        print(f'zoom {z}: {count} tiles')

    path = os.path.join(o.out, 'basemaps.json')
    maps = json.load(open(path)) if o.append and os.path.exists(path) else []
    maps = [m for m in maps if m.get('mapId') != o.map_id]
    num = lambda v: int(v) if float(v).is_integer() else v
    maps.append({'mapId': o.map_id, 'name': o.name, 'bounds': [[num(o.left), num(o.bottom)], [num(o.right), num(o.top)]],
                 'center': [round((o.left + o.right) / 2), round((o.bottom + o.top) / 2)], 'defaultPlane': o.plane})
    json.dump(maps, open(path, 'w'), indent='\t')
    print('wrote', path)


if __name__ == '__main__':
    main()

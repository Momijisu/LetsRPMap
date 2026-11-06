#!/usr/bin/env python3
"""Make stand-in test tiles (a labelled GTA-coordinate grid) without a real map:
    python3 stand_in_tiles.py out
"""
# Stand-in tiles in the fork's layout: {mapID}/{z}/{plane}_{x}_{-y}.png, where one
# map unit = one GTA metre (x east, y north), 256px tiles, scale 2^z px per metre.
import os, math, json, sys
from PIL import Image, ImageDraw
out = sys.argv[1]
X0, X1, Y0, Y1 = -4000, 4500, -4000, 8000
places = {'Airport': (-1200, -2800), 'Vinewood sign': (700, 1200), 'Sandy Shores': (1800, 3700), 'Paleto Bay': (-200, 6400)}
for z in (-3, -2, -1, 0):
    s = 2 ** z; T = 256 / s
    for i in range(math.floor(X0 / T), math.ceil(X1 / T)):
        for j in range(math.floor(Y0 / T), math.ceil(Y1 / T)):
            im = Image.new('RGB', (256, 256), (22, 26, 34)); d = ImageDraw.Draw(im)
            px = lambda x: (x - i * T) * s
            py = lambda y: ((j + 1) * T - y) * s
            step = 500 if z >= -1 else 1000
            for gx in range(int(X0 // step * step), X1 + 1, step):
                d.line([(px(gx), 0), (px(gx), 256)], fill=(60, 70, 90) if gx else (200, 80, 80))
            for gy in range(int(Y0 // step * step), Y1 + 1, step):
                d.line([(0, py(gy)), (256, py(gy))], fill=(60, 70, 90) if gy else (200, 80, 80))
            for name, (x, y) in places.items():
                cx, cy = px(x), py(y)
                if -40 < cx < 296 and -40 < cy < 296:
                    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(250, 200, 60)); d.text((cx + 8, cy - 6), name, fill=(250, 220, 120))
            d.text((4, 4), f'z{z} x{i} y{j}', fill=(90, 100, 120))
            path = f'{out}/0/{z}'; os.makedirs(path, exist_ok=True)
            im.save(f'{path}/0_{i}_{j}.png')
json.dump([{'mapId': 0, 'name': 'Los Santos', 'bounds': [[X0, Y0], [X1, Y1]], 'center': [0, 1000], 'defaultPlane': 0}], open(f'{out}/basemaps.json', 'w'))
print('done')

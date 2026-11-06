# Let's RP Map (Kartographer)

Interactive maps of Los Santos and Blaine County for the
[Let's RP Wiki](https://letsrpwiki0383.live-website.com/), a MediaWiki extension.

This is a fork of [Weird Gloop's Kartographer](https://github.com/weirdgloop/mediawiki-extensions-Kartographer),
the version the RuneScape wikis use for their game maps, which is itself a fork of
Wikimedia's [Kartographer](https://www.mediawiki.org/wiki/Extension:Kartographer).
Licensed GPL-3.0 (see `LICENSE`).

## Branches

| Branch | What it is |
|---|---|
| `weirdgloop/REL1_45` | Weird Gloop's code, unchanged. Update it from upstream, then merge into `LetsRPMap`. |
| `LetsRPMap` | Our changes. Install this one. |

To pull in Weird Gloop's latest changes:

```bash
git remote add weirdgloop https://github.com/weirdgloop/mediawiki-extensions-Kartographer.git
git fetch weirdgloop weirdgloop/REL1_45
git checkout weirdgloop/REL1_45 && git merge --ff-only weirdgloop/weirdgloop/REL1_45 && git push
git checkout LetsRPMap && git merge weirdgloop/REL1_45
```

## How it works

* Maps use **GTA world coordinates**: one map unit is one metre, `x` runs east and `y`
  runs north, the same numbers players see in game.
* The map pictures are an ordinary web-map tile set (256 px tiles, zoom 0 = the whole
  map in one tile), used **unchanged**, in a folder on the wiki's own server (`/tiles/`).
  No tile server or other service is needed.
* Four numbers, `transformation`, line the tiles up with GTA coordinates. Weird Gloop's
  version only takes tiles cut in RuneScape's own layout; this fork adds `transformation`,
  `worldBounds`, `minZoom` and `maxZoom` settings so it can use standard tile sets.
* `/tiles/basemaps.json` lists the maps (normally just one, Los Santos);
  `tools/basemaps.json` is ready to use.

### The Let's RP tiles

Road-map style JPEGs named `{z}_{x}_{y}.jpg` (e.g. `7_71_88.jpg`), zoom 0 to 7, all in one
folder. Zoom 7 is about 1.6 pixels per metre.

### Calibration

`transformation` is `[a, b, c, d]`: a tile pixel for GTA position (x, y) at zoom z is
`((a * x + b) * 2^z, (c * y + d) * 2^z)`. The defaults,

```
[ 0.0125265, 121.43, -0.0125265, 155.2606 ]
```

were fitted to in-game readings at five landmarks (port pier corners, Paleto Bay tip, a
north-west pier and the Fort Zancudo runway end). Every landmark lands within 10-20 m. To
make it more exact, take more in-game readings at sharp corners, find the same points on
zoom 6 or 7 tiles, and refit; only these four numbers change, never the tiles or the
coordinates written in articles.

### Other tile sets

`tools/` also has scripts for tile sets in other layouts:

* `stitch_xyz.py`: joins one zoom level of a tile set (`{z}/{x}/{y}.png` folders, or flat
  files with e.g. `--pattern "{z}_{x}_{y}.jpg"`) into one picture.
* `cut_tiles.py`: cuts a big picture into tiles in the RuneScape layout
  (`{mapID}/{z}/{plane}_{x}_{y}.png`, one unit = one metre at zoom 0), for use without
  `transformation`.
* `stand_in_tiles.py`: makes a labelled test grid in that layout.

## Installing on the wiki (no shell needed)

1. Download this repository's `LetsRPMap` branch and upload it to `extensions/Kartographer/`.
2. Upload the tile set, unchanged, to a `tiles/` folder next to `index.php`, plus
   `tools/basemaps.json`.
3. Add to `LocalSettings.php` (see `tools/LocalSettings.example.php` to change anything):
   ```php
   wfLoadExtension( 'Kartographer' );
   $wgKartographerMapServer = '';
   ```
4. Run the database update: `/mw-config/index.php` in a browser (it asks for
   `$wgUpgradeKey` from `LocalSettings.php`), or `php maintenance/run.php update`.

Requires MediaWiki 1.43 or newer (the wiki runs 1.46). Composer package:
`justinrainbow/json-schema` (MediaWiki usually includes it already).

## Using maps in articles

A map in the page, centred on a place, with a pin:

```wikitext
<mapframe x=-1200 y=-2800 zoom=2 width=400 height=300 mapID=0 plane=0 text="Los Santos International Airport">
{
  "type": "Feature",
  "geometry": { "type": "Point", "coordinates": [ -1200, -2800 ] },
  "properties": { "title": "Los Santos International Airport" }
}
</mapframe>
```

A link that opens the full-screen map:

```wikitext
<maplink x=-1200 y=-2800 zoom=2 mapID=0 plane=0 text="Show on map" />
```

Coordinates in the pin data are `[ x, y ]`. Pins, lines and areas use
[GeoJSON](https://geojson.org/), as on the RuneScape wikis
([how they use it](https://runescape.wiki/w/RuneScape:Map)).

## Changes from Weird Gloop's version

* Default settings point at the wiki's own `/tiles/` folder instead of RuneScape's map server.
* New settings `transformation`, `worldBounds`, `minZoom` and `maxZoom` (`modules/box/Map.js`),
  so a standard tile set can be used with game coordinates. Without them it works as before.
* English messages and the map picker say Let's RP / Los Santos instead of RuneScape.
* `tools/`: calibration-ready `basemaps.json`, settings example, and scripts for other tile layouts.

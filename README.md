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
* The map pictures are plain image **tiles** in a folder on the wiki's own server
  (`/tiles/`); no tile server or other service is needed.
* `/tiles/basemaps.json` lists the maps (normally just one, Los Santos).

### Tiles

Tiles are 256 px. At zoom `z` a tile covers `256 / 2^z` metres, and is saved as

```
tiles/{mapID}/{z}/{plane}_{x}_{y}.png
```

`tools/` makes them:

* `stitch_xyz.py`: joins one zoom level of an ordinary web-map tile set (`{z}/{x}/{y}.png` folders, or flat files like `7_71_88.jpg` with `--pattern "{z}_{y}_{x}.jpg"`)
  into one big picture.
* `cut_tiles.py`: cuts a big picture into tiles in our layout and writes `basemaps.json`.
  It needs the GTA coordinates of the picture's four edges.
* `stand_in_tiles.py`: makes a labelled test grid, for trying things out without a map.

**Lining up the coordinates:** find two places that are easy to spot on the picture and
whose GTA coordinates you know (e.g. the end of an airport runway and a pier). From each
place's pixel position and its coordinates, work out the metres per pixel and so the
coordinates of the picture's edges. Cut a low zoom first, check a few places on the map
with `<mapframe>`, and adjust.

## Installing on the wiki (no shell needed)

1. Download this repository's `LetsRPMap` branch and upload it to `extensions/Kartographer/`.
2. Upload the cut tiles and `basemaps.json` to a `tiles/` folder next to `index.php`.
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
* English messages and the map picker say Let's RP / Los Santos instead of RuneScape.
* `tools/` for making tiles in GTA coordinates.

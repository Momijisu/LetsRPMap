<?php
// Add to LocalSettings.php. The defaults (extension.json) already expect the
// Let's RP tiles, unchanged, in /tiles/ on the wiki's own server; change these
// only if your tiles live somewhere else or you re-calibrate.
wfLoadExtension( 'Kartographer' );
$wgKartographerMapServer = '';
$wgKartographerDataConfig = [
	// The tile sets, each a folder of {z}_{x}_{y}.jpg files. With more than one,
	// every map gets a switch (Atlas | Satellite); the first is the default.
	'tileLayers' => [
		[ 'name' => 'Atlas', 'url' => '/tiles/atlas/' ],
		[ 'name' => 'Satellite', 'url' => '/tiles/satellite/' ],
	],
	'baseTileURL' => '/tiles/atlas/',           // used when tileLayers isn't set
	'basePlainTileURL' => '/tiles/atlas/',
	'tileURLFormat' => '{z}_{x}_{y}.jpg',       // the tile files' names
	'baseMapsFile' => '/tiles/basemaps.json',   // the list of maps (tools/basemaps.json)
	'wikiImageURL' => '/images/',
	'attribution' => "Let's RP Wiki",
	'mapVersion' => '1',
	// Lines the tiles up with GTA world coordinates: a tile pixel at zoom z is
	// ((a * x + b) * 2^z, (c * y + d) * 2^z). Fitted from in-game readings at
	// five landmarks, accurate to about 10-20 m. See README to refine it.
	'transformation' => [ 0.0125265, 121.43, -0.0125265, 155.2606 ],
	// The area the zoom-0 tile covers, in GTA metres: [[minX, minY], [maxX, maxY]]
	'worldBounds' => [ [ -9694, -8042 ], [ 10743, 12395 ] ],
	'minZoom' => 0,
	'maxZoom' => 8,          // one step past the tiles, slightly enlarged
	'maxNativeZoom' => 7,    // the most detailed zoom in the tile set
	'tileSize' => 256,
	'planes' => false,       // RuneScape's floor control: GTA has one level
	'mapSelect' => false,    // the map picker: only useful with several maps
	// 'standaloneURL' => '', // a separate map site: shows an "External maps" button
];

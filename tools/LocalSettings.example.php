<?php
// Add to LocalSettings.php. The defaults already expect tiles in /tiles/ on the
// wiki's own server; change these only if your tiles live somewhere else.
wfLoadExtension( 'Kartographer' );
$wgKartographerMapServer = '';
$wgKartographerDataConfig = [
	'baseTileURL' => '/tiles/',                 // folder holding {mapID}/{z}/...
	'basePlainTileURL' => '/tiles/',
	'tileURLFormat' => '{mapID}/{z}/{p}_{x}_{-y}.png',
	'baseMapsFile' => '/tiles/basemaps.json',   // the list of maps (cut_tiles.py writes it)
	'wikiImageURL' => '/images/',
	'attribution' => "Let's RP Wiki",
	'mapVersion' => '1',
	'maxNativeZoom' => 3,                       // the most detailed zoom you cut
	'tileSize' => 256,
];

# Terrain and Imagery Utils

Convert GeoTIFF files between different projection system, make GeoTIFF files do linear translation

## Prerequisites

### Python >= 3.8

### Dependencies

```shell
$ pip install -r requirements.txt
```

## Usage

Imaging we have a terrain named `terrain.tif` and an imagery file named `imagery.tif` in Beijing 54 projection system
with some drift. And we want to use them in Cesium ion as assets files.

### Step 0 (Optional): change resolution

```shell
$ python change_resolution.py --ratio 0.75 --src-filename mosaic.tif --dst-filename imagery.tif
$ python change_resolution.py --ratio 0.75 --src-filename dsm.tif --dst-filename terrain.tif
```

### Step 1: reproject

```shell
$ python reproject.py --src-filename imagery.tif  --dst-filename temp_img.tif
$ python reproject.py --src-filename terrain.tif  --dst-filename temp_terr.tif
```

### Step 2: measure the drift with temp_img.tif

You can measure the drift for both direction in QGIS. Get drift distance in meters.
Let's say we have drift in `x` direction is `50` meters, and in `y` direction is `75` meters.

### Step 3: correction and compression

```shell
$ python3 correct_and_compress.py --src-filename temp_img.tif --dst-filename imagery_wgs84.tif --dx-in-meters 50 --dy-in-meters 75
$ python3 correct_and_compress.py --src-filename temp_terr.tif --dst-filename terraim_wgs84.tif --dx-in-meters 50 --dy-in-meters 75
```

### Step 4: upload to Cesium

Upload the GeoTIFF files by their type.

**Attention**

When upload terrain files, remember to select `Base terrain` with `Cesium World Terrain`,
and `Height reference` with `Ellipsoid (WGS84)`.
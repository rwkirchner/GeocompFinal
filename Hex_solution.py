import geopandas as gpd
import rasterio
import numpy as np
from shapely.geometry import box
from shapely.ops import unary_union
from rasterstats import zonal_stats
import os

# ----------------------------
# CONFIGURATION
# ----------------------------

ndvi_path = "classes/geocomp/finalproj/outputs/ndvi_nyc_clipped.TIF"
lst_path = "classes/geocomp/finalproj/outputs/lst_nyc_clipped.TIF"
parks_path = "classes/geocomp/finalproj/outputs/Parks.geojson"
hex_output = "classes/geocomp/finalproj/outputs/hex_ndvi_lst_parks_filtered.geojson"
hex_size = 500  # meters

# ----------------------------
# 1. LOAD RASTER EXTENT & MAKE HEX GRID
# ----------------------------

with rasterio.open(ndvi_path) as src:
    bounds = src.bounds
    crs = src.crs

# Middle third X bounds
x_width_third = (bounds.right - bounds.left) / 3
xmin = bounds.left + x_width_third + 500
xmax = bounds.right - x_width_third + 500
ymin = bounds.bottom - 500
ymax = bounds.top + 500

width = hex_size * 2 / np.sqrt(3)
height = hex_size * 1.5

cols = int(np.ceil((xmax - xmin) / width)) + 1
rows = int(np.ceil((ymax - ymin) / height)) + 1

hexes = []
for row in range(rows):
    for col in range(cols):
        x = xmin + col * width
        y = ymin + row * height
        if row % 2 == 0:
            x += width / 2
        hex = box(x - hex_size, y - hex_size, x + hex_size, y + hex_size)
        hexes.append(hex)

hex_gdf = gpd.GeoDataFrame(geometry=hexes, crs=crs)
hex_gdf = hex_gdf[hex_gdf.intersects(box(xmin, ymin, xmax, ymax))].reset_index(drop=True)


centroids_y = hex_gdf.geometry.centroid.y
median_y = np.median(centroids_y)
hex_gdf = hex_gdf[hex_gdf.centroid.y <= median_y].reset_index(drop=True)

print("Calculating mean NDVI...")
ndvi_stats = zonal_stats(hex_gdf, ndvi_path, stats="mean", geojson_out=False, nodata=np.nan)
hex_gdf["ndvi"] = [x["mean"] if x["mean"] is not None else np.nan for x in ndvi_stats]

print("Calculating mean LST...")
lst_stats = zonal_stats(hex_gdf, lst_path, stats="mean", geojson_out=False, nodata=np.nan)
hex_gdf["lst"] = [x["mean"] if x["mean"] is not None else np.nan for x in lst_stats]


print("Calculating % park coverage...")
parks = gpd.read_file(parks_path).to_crs(crs)
hex_area = hex_gdf.geometry.area
parks_union = unary_union(parks.geometry)
intersect_area = hex_gdf.geometry.intersection(parks_union).area
hex_gdf["pct_park"] = (intersect_area / hex_area) * 100


os.makedirs(os.path.dirname(hex_output), exist_ok=True)
hex_gdf.to_file(hex_output, driver="GeoJSON")
print(f"✅ Final filtered hex grid saved to: {hex_output}")

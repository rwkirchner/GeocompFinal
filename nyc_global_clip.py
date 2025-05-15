import rasterio
from rasterio.mask import mask
from shapely.geometry import box, mapping
import fiona
import os


nyc_bounds = (-74.3, 40.45, -73.65, 40.95)

# Convert to a shapely polygon and then GeoJSON-style mapping
nyc_bbox = box(*nyc_bounds)
nyc_geojson = [mapping(nyc_bbox)]

# --- Input: path to your global VIIRS LST/NDVI raster ---
input_raster_path = "global_viirs_LST_or_NDVI.tif"  # Replace with your actual file path
output_raster_path = "nyc_clipped_viirs.tif"

# --- Clip the raster ---
with rasterio.open(input_raster_path) as src:
    out_image, out_transform = mask(src, nyc_geojson, crop=True)
    out_meta = src.meta.copy()

# --- Update metadata for new raster ---
out_meta.update({
    "driver": "GTiff",
    "height": out_image.shape[1],
    "width": out_image.shape[2],
    "transform": out_transform
})

# --- Save clipped raster ---
with rasterio.open(output_raster_path, "w", **out_meta) as dest:
    dest.write(out_image)

print("✅ Clipped raster saved to:", output_raster_path)

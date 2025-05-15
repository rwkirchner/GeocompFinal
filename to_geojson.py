import numpy as np
import rasterio
from shapely.geometry import box, mapping
from rasterio.mask import mask
from rasterio.features import shapes
import geopandas as gpd
import os

# File paths
ndvi_path = "classes/geocomp/finalproj/outputs/ndvi_nyc_clipped.TIF"
lst_path = "classes/geocomp/finalproj/outputs/lst_nyc_clipped.TIF"

ndvi_out_geojson = "classes/geocomp/finalproj/outputs/ndvi_clipped_simplified.geojson"
lst_out_geojson = "classes/geocomp/finalproj/outputs/lst_clipped_simplified.geojson"

# Output folder
os.makedirs("classes/geocomp/finalproj/outputs", exist_ok=True)

def clip_and_export(tif_path, geojson_out, field_name, simplify_tolerance=10):
    with rasterio.open(tif_path) as src:
        bounds = src.bounds
        width_third = (bounds.right - bounds.left) / 3

        # Middle third horizontally
        minx = bounds.left + width_third
        maxx = bounds.right - width_third
        miny = bounds.bottom
        maxy = bounds.top

        bbox_geom = [mapping(box(minx, miny, maxx, maxy))]

        out_image, out_transform = mask(src, bbox_geom, crop=True)
        out_image = np.squeeze(out_image)
        mask_array = ~np.isnan(out_image)

        results = (
            {"properties": {field_name: float(val)}, "geometry": geom}
            for geom, val in shapes(out_image, mask=mask_array, transform=out_transform)
        )

        gdf = gpd.GeoDataFrame.from_features(results)
        gdf.crs = src.crs

        y_medians = [geom.centroid.y for geom in gdf.geometry]
        median_y = np.median(y_medians)
        gdf = gdf[gdf.geometry.centroid.y <= median_y]

        # Simplify geometry (10m tolerance)
        gdf["geometry"] = gdf["geometry"].simplify(tolerance=simplify_tolerance, preserve_topology=True)

        gdf.to_file(geojson_out, driver="GeoJSON")
        print(f"✅ Simplified and exported {field_name} to:", geojson_out)

clip_and_export(ndvi_path, ndvi_out_geojson, field_name="NDVI")
clip_and_export(lst_path, lst_out_geojson, field_name="LST_C")

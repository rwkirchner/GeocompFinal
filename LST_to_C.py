import rasterio
import numpy as np
import os
from rasterio.features import shapes
import geopandas as gpd
from shapely.geometry import shape


b10_path = "classes/geocomp/finalproj/SurfaceTemp.TIF"
tif_out = "classes/geocomp/finalproj/outputs/lst_nyc.TIF"
vector_out = "classes/geocomp/finalproj/outputs/lst_vector.geojson"

EXPORT_AS_VECTOR = True  # Change to False to skip vector export

with rasterio.open(b10_path) as src:
    raw = src.read(1).astype('float32')

    lst_c = raw * 0.00341802 - 273.15
    lst_c = np.where(raw == 0, np.nan, lst_c) 

    profile = src.profile
    profile.update(dtype=rasterio.float32, count=1)

    os.makedirs("classes/geocomp/finalproj/outputs", exist_ok=True)

    with rasterio.open(tif_out, 'w', **profile) as dst:
        dst.write(lst_c, 1)

    print("✅ LST (°C) saved to:", tif_out)


if EXPORT_AS_VECTOR:
    print("🌀 Converting raster to vector polygons...")

    with rasterio.open(tif_out) as src:
        lst_data = src.read(1)
        mask = lst_data != src.nodata

        results = (
            {"properties": {"LST_C": float(val)}, "geometry": geom}
            for geom, val in shapes(lst_data, mask=mask, transform=src.transform)
        )

        gdf = gpd.GeoDataFrame.from_features(results)
        gdf.crs = src.crs

        gdf = gdf[(gdf["LST_C"] > -20) & (gdf["LST_C"] < 60)]

        gdf.to_file(vector_out, driver="GeoJSON")
        print("✅ Vector LST saved to:", vector_out)

import rasterio
import numpy as np
import os
from rasterio.features import shapes
import geopandas as gpd

b4_path = "classes/geocomp/finalproj/SR_B4.TIF"
b5_path = "classes/geocomp/finalproj/SR_B5.TIF"
tif_out = "classes/geocomp/finalproj/outputs/ndvi_nyc.TIF"
vector_out = "classes/geocomp/finalproj/outputs/ndvi_vector.geojson"

with rasterio.open(b4_path) as red_src, rasterio.open(b5_path) as nir_src:
    red = red_src.read(1).astype('float32')
    nir = nir_src.read(1).astype('float32')
    ndvi = (nir - red) / (nir + red)
    ndvi = np.where((nir + red) == 0, np.nan, ndvi)
    profile = red_src.profile
    profile.update(dtype=rasterio.float32, count=1)
    os.makedirs("classes/geocomp/finalproj/outputs", exist_ok=True)
    with rasterio.open(tif_out, 'w', **profile) as dst:
        dst.write(ndvi, 1)

with rasterio.open(tif_out) as src:
    ndvi_data = src.read(1)
    mask = ndvi_data != src.nodata
    results = (
        {"properties": {"NDVI": float(val)}, "geometry": geom}
        for geom, val in shapes(ndvi_data, mask=mask, transform=src.transform)
    )
    gdf = gpd.GeoDataFrame.from_features(results)
    gdf.crs = src.crs
    gdf = gdf[(gdf["NDVI"] > -1) & (gdf["NDVI"] < 1)]
    gdf.to_file(vector_out, driver="GeoJSON")

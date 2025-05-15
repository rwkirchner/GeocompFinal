import geopandas as gpd
import numpy as np
import pandas as pd
from libpysal.weights import KNN
from spreg import ML_Lag


gdf = gpd.read_file("classes/geocomp/finalproj/outputs/hex_ndvi_lst_parks_filtered.geojson")


df = gdf[['ndvi', 'pct_park', 'lst']].dropna()
gdf = gdf.loc[df.index].reset_index(drop=True)


print("🔗 Building KNN weights...")
w = KNN.from_dataframe(gdf, k=6)
w.transform = 'r'



y = df['lst'].values.reshape((-1, 1))  
X = df[['ndvi', 'pct_park']].values   



print("📊 Running spatial lag regression...")
model = ML_Lag(y, X, w=w, name_y='LST', name_x=['NDVI', 'Pct_Park'])



print("✅ Spatial Regression Summary:")
print(model.summary)

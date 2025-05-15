import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt


gdf = gpd.read_file("classes/geocomp/finalproj/outputs/hex_ndvi_lst_parks_filtered.geojson")

gdf["lst_c"] = (gdf["lst"] * 0.00341802) - 273.15


df = gdf[['ndvi', 'lst_c']].dropna()
sns.scatterplot(data=df, x="ndvi", y="lst_c", s=30)
plt.title("NDVI vs. Land Surface Temperature (°C)")
plt.xlabel("NDVI")
plt.ylabel("LST (°C)")
plt.tight_layout()
plt.show()

import geopandas as gpd
import matplotlib.pyplot as plt

# Load NYC Parks
parks = gpd.read_file("classes/geocomp/finalproj/Parks.geojson")

# Preview
print(parks.head())
print(parks.crs)  # Coordinate reference system


# Plot
parks.plot(figsize=(10, 10), edgecolor='black', facecolor='green', alpha=0.5)
plt.title("NYC Parks and Open Space")
plt.show()
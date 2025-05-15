import numpy as np
import rasterio
from shapely.geometry import box, mapping
from rasterio.mask import mask
import matplotlib.pyplot as plt

tif_path = "classes/geocomp/finalproj/outputs/ndvi_nyc_clipped.TIF"

with rasterio.open(tif_path) as src:
    bounds = src.bounds
    width_third = (bounds.right - bounds.left) / 3

    minx = bounds.left + width_third
    maxx = bounds.right - width_third
    miny = bounds.bottom
    maxy = bounds.top

    bbox_geom = [mapping(box(minx, miny, maxx, maxy))]

    out_image, out_transform = mask(src, bbox_geom, crop=True)
    out_image = np.squeeze(out_image)

    # Get Y coordinates for each row to calculate median
    height = out_image.shape[0]
    y_coords = [out_transform * (0, row) for row in range(height)]
    y_vals = [y for (x, y) in y_coords]
    median_y = np.median(y_vals)

    # Get indices below the median Y
    keep_rows = [i for i, y in enumerate(y_vals) if y <= median_y]
    cropped_image = out_image[keep_rows, :]

# Plot the cropped raster
plt.figure(figsize=(8, 10))
plt.imshow(cropped_image, cmap="YlGn", vmin=-1, vmax=1)
plt.title("NDVI Raster – Middle Third X, Bottom Half Y")
plt.axis("off")
plt.tight_layout()
plt.show()


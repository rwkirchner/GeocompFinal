import rasterio
import matplotlib.pyplot as plt
import numpy as np
from rasterio.plot import plotting_extent

with rasterio.open("classes/geocomp/finalproj/outputs/ndvi_nyc.TIF") as ndvi_src:
    ndvi = ndvi_src.read(1)
    ndvi_extent = plotting_extent(ndvi_src)

with rasterio.open("classes/geocomp/finalproj/outputs/lst_nyc.TIF") as lst_src:
    lst = lst_src.read(1)
    lst_extent = plotting_extent(lst_src)

rows, cols = ndvi.shape
r_end = rows // 2
c_end = cols // 2

ndvi_crop = ndvi[:r_end, :c_end]
lst_crop = lst[:r_end, :c_end]

ndvi_xmin, ndvi_xmax = ndvi_extent[0], ndvi_extent[0] + (ndvi_extent[1] - ndvi_extent[0]) / 2
ndvi_ymin, ndvi_ymax = ndvi_extent[2] + (ndvi_extent[3] - ndvi_extent[2]) / 2, ndvi_extent[3]
ndvi_crop_extent = (ndvi_xmin, ndvi_xmax, ndvi_ymin, ndvi_ymax)

lst_xmin, lst_xmax = lst_extent[0], lst_extent[0] + (lst_extent[1] - lst_extent[0]) / 2
lst_ymin, lst_ymax = lst_extent[2] + (lst_extent[3] - lst_extent[2]) / 2, lst_extent[3]
lst_crop_extent = (lst_xmin, lst_xmax, lst_ymin, lst_ymax)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ndvi_im = ax1.imshow(ndvi_crop, cmap="YlGn", extent=ndvi_crop_extent, vmin=-1, vmax=1)
ax1.set_title("NDVI (Top-Left Quarter)")
fig.colorbar(ndvi_im, ax=ax1, orientation="vertical", label="NDVI")

lst_im = ax2.imshow(lst_crop, cmap="inferno", extent=lst_crop_extent)
ax2.set_title("LST (°C) - Top-Left Quarter")
fig.colorbar(lst_im, ax=ax2, orientation="vertical", label="°C")

plt.tight_layout()
plt.show()

# GeocompFinal
LST_to_C.py – Converts raw LST raster values to Celsius and exports the result.

ndvi_process.py – Computes NDVI from red/NIR bands and saves the output raster.

nyc_global_clip.py – Clips global rasters down to the NYC region using bounding box masking.

parksvis.py – Visualizes NYC park polygons overlaid on a base map.

reproj.py – Reprojects vector or raster data into a consistent CRS (e.g., EPSG:32618).

scatterplot.py – Plots NDVI vs. LST scatterplot using hexagon-aggregated data.

stats.py – Runs correlation and regression analyses (linear and spatial) on the hex grid data.

to_geojson.py – Converts clipped NDVI/LST rasters into simplified vector GeoJSONs for mapping.

Visual.py – Displays visualizations of NDVI and LST side-by-side for initial raster inspection.

This project analyzes the relationship between vegetation and urban heat in New York City using satellite-derived data on land surface temperature (LST) and the Normalized Difference Vegetation Index (NDVI). By preprocessing Landsat 9 imagery and NYC parks data, I calculated NDVI and converted raw thermal band values to Celsius, clipped and reprojected the datasets, and conducted preliminary visualizations. Initially, I attempted to convert raster layers to GeoJSONs for web mapping, but the vector file sizes were too large to be practical. This led to the adoption of a hexagonal grid approach to spatially aggregate NDVI, LST, and park coverage metrics across the city.

The project then used both standard linear regression and spatial lag models to quantify how vegetation affects temperature. Results showed a significant negative correlation between NDVI and LST, confirming that real vegetative cover—not just park boundaries—drives urban cooling. Spatial regression revealed strong spatial dependence (ρ = 0.98), validating the model choice. Final visualizations exposed inequities in urban heat exposure, showing that lower-income neighborhoods tend to have less greenery and higher temperatures. These findings underscore the importance of prioritizing vegetation-based climate interventions in underserved areas to enhance resilience and promote environmental equity across NYC.

from osgeo import ogr

# Define the WKT string
wktstring = "POINT (1120351.5712494177 741921.4223245403)"

# Transform to a GDAL (OGR) object
point = ogr.CreateGeometryFromWkt(wktstring)

# Get properties
print(type(point))
print("%d,%d" % (point.GetX(), point.GetY()))

from shapely.geometry import Point
from shapely.wkt import loads

# Create point from WKT string 
wktstring = 'POINT(173994.1578792833 444133.6032947102)'
wageningen_campus = loads(wktstring)
print(type(wageningen_campus))

# Point directly
wageningen_campus = Point([173994.1578792833, 444133.60329471016])
print(type(wageningen_campus))

import geopandas as gpd
from shapely.wkt import loads

# Define a point
wktstring = 'POINT(173994.1578792833 444133.6032947102)'

# Convert to a GeoSeries
gs = gpd.GeoSeries([loads(wktstring)])

# Inspect the properties
print(type(gs), len(gs))

# Specify the projection
gs.crs = "EPSG:28992" 

# We can now apply a function
# As an example, we add a buffer of 100 m
gs_buffer = gs.buffer(100)

# Inspect the results
print(gs.geometry)
print(gs_buffer.geometry)

import pandas as pd

# Create some data, with three points, a, b, and c.
data = {'name': ['a', 'b', 'c'],
        'x': [173994.1578792833, 173974.1578792833, 173910.1578792833],
        'y': [444135.6032947102, 444186.6032947102, 444111.6032947102]}

# Turn the data into a Pandas DataFrame (column names are extracted automatically)
df = pd.DataFrame(data)

# Inspect the DataFrame
print(df.head)

# Use the coordinates to make shapely Point geometries
geometry = [Point(xy) for xy in zip(df['x'], df['y'])]

# Pandas DataFrame and shapely Points can together become a GeoPandas GeoDataFrame
# Note that we specify the CRS (projection) directly while creating a GDF
wageningenGDF = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:28992") 

# Inspect wageningenGDF
print(type(wageningenGDF), len(wageningenGDF))

from matplotlib import pyplot as plt

# Plotting a map of the GeoDataFrame directly
wageningenGDF.plot(marker='*', color='green', markersize=50)

# Check the current crs
print(wageningenGDF.crs)

# Re-project the points to WGS84
wageningenGDF = wageningenGDF.to_crs('EPSG:4326')

# Check the crs again to see if the changes were succesful
print(wageningenGDF.crs)

# Save to disk
# wageningenGDF.to_file(filename='data/wageningenPOI.geojson', driver='GeoJSON')
# wageningenGDF.to_file(filename='data/wageningenPOI.shp', driver='ESRI Shapefile')

# Read from disk
jsonGDF = gpd.read_file('data/wageningenPOI.geojson')
shpGDF = gpd.read_file('data/wageningenPOI.shp')
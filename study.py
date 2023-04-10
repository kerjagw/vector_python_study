#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 07:23:53 2023
@author: beasiswa4@dekstop.geo-circle.com
"""

import json
from owslib.wfs import WebFeatureService
import geopandas as gpd
import matplotlib.pyplot as plt


# Get the WFS of the BAG
wfsUrl = 'https://service.pdok.nl/lv/bag/wfs/v2_0'
wfs = WebFeatureService(url=wfsUrl, version='2.0.0')
layer = list(wfs.contents)[0]

# Define center point and create bbox for study area
x, y = (173994.1578792833, 444133.60329471016)
xmin, xmax, ymin, ymax = x - 500, x + 500, y - 500, y + 500

# Get the features for the study area
# notice that we now get them as json, in contrast to before
response = wfs.getfeature(typename=layer, bbox=(xmin, ymin, xmax, ymax), outputFormat='json')
data = json.loads(response.read())

# Create GeoDataFrame, without saving first
buildingsGDF = gpd.GeoDataFrame.from_features(data['features'])

# Set crs to RD New
buildingsGDF.crs = 28992

# Read in again with GeoPandas
roadsGDF = gpd.read_file('data/Roads.gml')

# Inspect and plot to get a quick view
print(type(roadsGDF))
roadsGDF.plot()
# plt.show()

# Plot roads and buildings together
roadlayer = roadsGDF.plot(color='grey')
buildingsGDF.plot(ax=roadlayer, color='red')

# Set the limits of the x and y axis
roadlayer.set_xlim(xmin, xmax)
roadlayer.set_ylim(ymin, ymax)

# Pandas function that returns the column labels of the DataFrame
print(buildingsGDF.columns)

# Pandas function that returns the first n rows, default n = 5
print(buildingsGDF.head())

# shape area (in the units of the projection)
print(buildingsGDF.area)

# Inspect building year column
print(buildingsGDF['bouwjaar'])

# Inspect first
print(buildingsGDF.area > 1000)

# Make the selection, select all rows with area > 1000 m2, and all columns
# Using 'label based' indexing with loc, here with a Boolean array
largeBuildingsGDF = buildingsGDF.loc[buildingsGDF.area > 1000, :]

# Plot
largeBuildingsGDF.plot()

# Inspect first
print(buildingsGDF['status'].isin(['Bouw gestart']))

# Make the selection, the list of required values can contain more than one item
newBuildingsGDF = buildingsGDF[buildingsGDF['status'].isin(['Bouw gestart'])]

# Plot the new buildings with a basemap for reference
# based on https://geopandas.org/gallery/plotting_basemap_background.html
import contextily as ctx

# Re-project
newBuildingsGDF = newBuildingsGDF.to_crs(epsg=3857)

# Plot with 50% transparency
ax = newBuildingsGDF.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
ctx.add_basemap(ax, source=ctx.providers.Stamen.TonerLite, zoom=17)
ax.set_axis_off()

# Save the figure to disk
plt.savefig('./output/StudyArea.png')
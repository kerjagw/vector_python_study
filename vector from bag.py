import json
from owslib.wfs import WebFeatureService
import geopandas as gpd
import matplotlib.pyplot as plt

# Read in again with GeoPandas
roadsGDF = gpd.read_file('data/Roads.gml')

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

# Plot roads and buildings together
roadlayer = roadsGDF.plot(color='grey')
buildingsGDF.plot(ax=roadlayer, color='red')

# Set the limits of the x and y axis
roadlayer.set_xlim(xmin, xmax)
roadlayer.set_ylim(ymin, ymax)

# Save the figure to disk
plt.savefig('./output/BuildingsAndRoads.png')

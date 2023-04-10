from owslib.wfs import WebFeatureService
import geopandas as gpd
import matplotlib as plt

# Put the WFS url in a variable
wfsUrl = 'https://geodata.nationaalgeoregister.nl/nwbwegen/wfs?'

# Create a WFS object
wfs = WebFeatureService(url=wfsUrl, version='2.0.0')

# Get the title from the object
print(wfs.identification.title)

# Check the contents of the WFS
print(list(wfs.contents))

# Define center point and create bbox for study area
x, y = (173994.1578792833, 444133.60329471016)
xmin, xmax, ymin, ymax = x - 1000, x + 350, y - 1000, y + 350

# Get the features for the study area (using the wfs from the previous code block)
response = wfs.getfeature(typename=list(wfs.contents)[0], bbox=(xmin, ymin, xmax, ymax))

# Save them to disk
with open('data/Roads.gml', 'wb') as file:
    file.write(response.read())

# Read in again with GeoPandas
roadsGDF = gpd.read_file('data/Roads.gml')

# Inspect and plot to get a quick view
print(type(roadsGDF))
roadsGDF.plot()
plt.show()

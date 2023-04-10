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


# BUFFER ROAD AND DISTANCE

print(type(roadsGDF))
print(type(roadsGDF.geometry))
print(roadsGDF['geometry'])

# Buffer of 1.5 m on both sides
roadsPolygonGDF = gpd.GeoDataFrame(roadsGDF, geometry=roadsGDF.buffer(distance=1.5)) 

# Plot
roadsPolygonGDF.plot(color='blue', edgecolor='blue')

# Check the total coverage of buffers
print(roadsPolygonGDF.area.sum())


# OSMNX

import osmnx as ox

# Using a geocoder to get the extent
city = ox.geocoder.geocode_to_gdf('Wageningen, Netherlands')
ox.plot.plot_footprints(ox.project_gdf(city))

# Get bike network and create graph
wageningenRoadsGraph = ox.graph.graph_from_place('Wageningen, Netherlands', network_type='bike')

# Plot and save
ox.plot.plot_graph(wageningenRoadsGraph, figsize=(10, 10), node_size=2)
ox.io.save_graph_shapefile(G=wageningenRoadsGraph, filepath='data/OSMnetwork_Wageningen.shp')

# Metadata
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G=wageningenRoadsGraph)
print(gdf_nodes.info())
print(gdf_edges.info())

# Origin
source = ox.distance.nearest_nodes(wageningenRoadsGraph, 5.665779, 51.987817)

# Destination
target = ox.distance.nearest_nodes(wageningenRoadsGraph, 5.662409, 51.964870)

# Compute shortest path 
shortestroute = ox.distance.shortest_path(G=wageningenRoadsGraph, orig=source, 
                                          dest=target, weight='length')

# Plot
ox.plot.plot_graph_route(wageningenRoadsGraph, shortestroute, figsize=(20, 20), 
                         route_alpha=0.6, route_color='darkred',  bgcolor='white', 
                         node_color='darkgrey', edge_color='darkgrey',
                         route_linewidth=10, orig_dest_size=100)

import folium

# Initialize the map
campusMap = folium.Map([51.98527485, 5.66370505205543], zoom_start=17)

# Re-project
buildingsGDF = buildingsGDF.to_crs(4326)
roadsPolygonGDF = roadsPolygonGDF.to_crs(4326)

# Add the buildings
folium.Choropleth(buildingsGDF, name='Building construction years',
                  data=buildingsGDF, columns=['identificatie', 'bouwjaar'],
                  key_on='feature.properties.identificatie', fill_color='RdYlGn',
                  fill_opacity=0.7, line_opacity=0.2,
                  legend_name='Construction year').add_to(campusMap)

# Add the roads
folium.GeoJson(roadsPolygonGDF).add_to(campusMap)

# Add layer control
folium.LayerControl().add_to(campusMap)

# Save (you can now open the generated .html file from the output directory)
campusMap.save('output/campusMap.html')
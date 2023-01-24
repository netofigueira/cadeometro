import osmnx as ox
from geopy.geocoders import Nominatim
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

geolocator = Nominatim(user_agent="geoapiExercises")

def nearest_subways(address):
    #geolocate the address
    location = geolocator.geocode(address)
    lat, lon = location.latitude, location.longitude
    #create a graph of the street network
    G = ox.graph_from_point((lat, lon), distance=2000, network_type='drive')
    #get the nearest nodes (subway stations)
    nearest_nodes = ox.get_nearest_nodes(G, (lat, lon), method='euclidean', return_dist=True)
    #sort the nodes by distance
    nearest_nodes = sorted(nearest_nodes, key=lambda x: x[1])
    #get the 3 nearest subway stations
    subways = []
    for i in range(3):
        #get the name of the subway station
        name = ox.get_node_attributes(G, 'name', nearest_nodes[i][0])
        subways.append({'name': name, 'distance': nearest_nodes[i][1]})
    return subways


geolocator = Nominatim(user_agent="geoapiExercises")

def get_subway_bounding_box(subway_name):
    location = geolocator.geocode(subway_name + ", São Paulo, Brazil")
    point = Point(location.longitude, location.latitude)
    print(point)
    buffer = point.buffer(0.0025)

    bounding_box = Polygon(buffer).bounds
    return bounding_box

"""
def search_subway_by_location(min_lat, min_lon, max_lat, max_lon):
    overpass = Overpass()
    overpass_query = f'node["railway"="subway_entrance"]({min_lat},{min_lon},{max_lat},{max_lon});out;'
    result = overpass.query(overpass_query)
    subways = [{'name': x.tags.get('name', 'unknown'), 'latitude': x.lat, 'longitude': x.lon} for x in result.nodes]
    return jsonify(subways)
"""


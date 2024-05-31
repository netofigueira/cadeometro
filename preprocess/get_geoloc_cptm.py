import pdfplumber
import pandas as pd
import googlemaps

df = pd.read_csv("linhas_cptm.csv")


def get_lat_long(station):
    api_key="AIzaSyCnMLVR8Ip3P5vZzuBx6Ct7kECl2YRAAbo"
    # Initialize the Google Maps client
    gmaps = googlemaps.Client(key=api_key)
    print(station)
    # Geocoding the address
    geocode_result = gmaps.geocode(station + ", São Paulo, Brasil")

    # Extract the latitude and longitude
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        return lat, lng
    else:
        return None, None





df[['latitude', 'longitude']] = df['estacao'].apply(lambda x: pd.Series(get_lat_long(x)))

df.to_csv('linhas_cptm_google.csv')
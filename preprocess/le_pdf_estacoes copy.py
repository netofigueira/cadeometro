import pdfplumber
import pandas as pd
import googlemaps

df = pd.read_csv("linhas_metro.csv")


def get_lat_long(address):
    api_key="AIzaSyCnMLVR8Ip3P5vZzuBx6Ct7kECl2YRAAbo"
    # Initialize the Google Maps client
    gmaps = googlemaps.Client(key=api_key)
    
    # Geocoding the address
    geocode_result = gmaps.geocode(address)
    
    # Extract the latitude and longitude
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        return lat, lng
    else:
        return None, None





df[['latitude', 'longitude']] = df['endereco'].apply(lambda x: pd.Series(get_lat_long(x)))

df['linhaID'] = df['linha'].apply(lambda x: x.split('-')[0][-1])
df['linhaID'] = df.linhaID.astype(int)
df.to_csv('linhas_metro_google.csv')
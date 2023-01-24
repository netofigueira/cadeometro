import pdfplumber
import pandas as pd

pdfs_path = 'Endereço das Estações.pdf'
df = pd.DataFrame()


from geopy.geocoders import Nominatim

from geopy.extra.rate_limiter import RateLimiter

geolocator = Nominatim(user_agent="geoapiExercises", timeout=10)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def get_address_coordinates(address):
    location = geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None

with pdfplumber.open(pdfs_path) as pdf:

    for page in pdf.pages:
        tablelist = page.extract_table()



        res = [[i[0], i[1]] for i in tablelist]


        aux = pd.DataFrame.from_records(res)
        aux.columns = ['estacao', 'endereco']

        aux['linha'] = aux.iloc[1, 0]
        df = pd.concat([df,aux])



df[['latitude', 'longitude']] = df['endereco'].apply(lambda x: pd.Series(get_address_coordinates(x)))

df['linhaID'] = df['linha'].apply(lambda x: x.split('-')[0][-1])
df['linhaID'] = df.linhaID.astype(int)
df.to_csv('linhas_metro.csv')
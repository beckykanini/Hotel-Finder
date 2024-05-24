import pandas as pd
import requests
import urllib.parse  # Import url parsing module

# Load your dataset
df = pd.read_csv("c:/Users/Rebecca/Trip Advisor Dataset/Reviews/Hotel_Features_Dataset.csv")
df.dropna(inplace=True)  # Drop missing values

df = df[['street']]

def geocode2(locality):
    request_url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(locality) +'?format=json'
    response = requests.get(request_url)
    if response.ok:
        try:
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon']
            else:
                return None, None
        except Exception as e:
            print(f"Error parsing response JSON: {e}")
            return None, None
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        return None, None

df['geocoded'] = df['street'].apply(geocode2)
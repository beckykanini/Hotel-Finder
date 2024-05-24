import json
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import scipy.sparse as sp

# Read data from the two files
df = pd.read_csv("C:/Users/Rebecca/Trip Advisor Dataset/Reviews/Hotel_Features_Dataset.csv")
data = pd.read_csv("C:/Users/Rebecca/feature_engineered.csv")

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        parsed_data = json.loads(post_data)
        print("Parsed data: ", parsed_data)
        
        # Extract user input from the parsed data
        hotel_features = parsed_data.get("hotel_features", "")
        hotel_input = parsed_data.get("hotel_input", "")
        location_input = parsed_data.get("location_input", "")
        print("Hotel Features Input:", hotel_features)
        print("Hotel Name Input:", hotel_input)
        print("Location Input:", location_input)
        
        # Concatenate features and handle missing values
        df['combined_features'] = df['country'].fillna('') + ' ' + df['amenities'].fillna('') + ' ' + df['rooms'].fillna('') + ' ' + df['types'].fillna('')

        # Function to preprocess text data
        def preprocess_text(text):
            if isinstance(text, str):
                return text.lower().strip()
            else:
                return ''
    
        # Function to get hotel recommendations based on combined amenities and location
        def get_hotel_recommendations(hotel_features, location_input):
            # Preprocess user input
            hotel_features = preprocess_text(hotel_features)
            location_input = preprocess_text(location_input)
            
            # Filter hotels by location
            df_filtered = df[df['country'].str.lower() == location_input]
            
            if df_filtered.empty:
                return ["No hotels found in the specified location."]
            
            # Initialize TF-IDF Vectorizer with sparse format
            vectorizer = TfidfVectorizer()
            features_matrix = vectorizer.fit_transform(df_filtered['combined_features'])
            
            # Convert TF-IDF matrix to sparse format
            features_matrix_sparse = sp.csr_matrix(features_matrix)
            
            # Train KNN model
            knn_model = NearestNeighbors(n_neighbors=4, algorithm='brute', metric='euclidean')
            knn_model.fit(features_matrix_sparse)
            
            # Transform user input into TF-IDF features
            user_features = vectorizer.transform([hotel_features])
            
            # Convert user features to sparse format
            user_features_sparse = sp.csr_matrix(user_features)
            
            # Find nearest neighbors using KNN
            distances, indices = knn_model.kneighbors(user_features_sparse)
            
            # Get recommended hotels with country
            recommended_hotels = []
            for index in indices[0]:
                hotel_name = df_filtered['name'].iloc[index]
                hotel_country = df_filtered['country'].iloc[index]
                hotel_rating = df_filtered['rating'].iloc[index]
                hotel_website = df_filtered['website'].iloc[index]  # Assuming the website URL is in the 'website' column
                recommended_hotels.append({
                    "name": hotel_name,
                    "country": hotel_country,
                    "rating": hotel_rating,
                    "website": hotel_website
                })
            
            return recommended_hotels

        # Function to get the location (latitude and longitude) of a place using Nominatim
        def get_location_from_nominatim(query):
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": query,
                "format": "json",
                "limit": 1
            }
            response = requests.get(url, params=params)
            if response.ok:
                data = response.json()
                if data:
                    return {
                        "latitude": data[0]['lat'],
                        "longitude": data[0]['lon']
                    }
            return None

        # Get hotel recommendations based on hotel features and location
        recommended_hotels = get_hotel_recommendations(hotel_features, location_input)
        
        # Fetching location for each recommended hotel
        for hotel_info in recommended_hotels:
            location_query = f"{hotel_info['name']}, {hotel_info['country']}"
            location = get_location_from_nominatim(location_query)
            if location:
                hotel_info["location"] = location

        # Prepare response
        response_data = {
            "recommended_hotels": recommended_hotels,
        }
        
        # Send the results back as JSON
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods", "POST")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

def run_server(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()

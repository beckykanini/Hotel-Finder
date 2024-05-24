from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import scipy.sparse as sp

# Sample hotel dataset
df = pd.read_csv("C:/Users/Rebecca/Trip Advisor Dataset/Reviews/Hotel_Features_Dataset.csv")

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        parsed_data = json.loads(post_data)
        print("Parsed data: ", parsed_data)
        
        # Extract user input from the parsed data
        user_input = parsed_data.get("user_input", "")
        
        # Function to preprocess text data
        def preprocess_text(text):
            if isinstance(text, str):
                return text.lower()
            else:
                return ''
        
        # Concatenate features and handle missing values
        df['combined_features'] = df['country'].fillna('') + ' ' + df['amenities'].fillna('') + ' ' + df['rooms'].fillna('') + ' ' + df['types'].fillna('')   
    
        # Function to get hotel recommendations based on combined amenities
        def get_hotel_recommendations(user_input):
            # Preprocess user input
            user_input = preprocess_text(user_input)
        
            # Initialize TF-IDF Vectorizer with sparse format
            vectorizer = TfidfVectorizer()
            features_matrix = vectorizer.fit_transform(df['combined_features'])
        
            # Convert TF-IDF matrix to sparse format
            features_matrix_sparse = sp.csr_matrix(features_matrix)
        
            # Train KNN model
            knn_model = NearestNeighbors(n_neighbors=4, algorithm='brute', metric='euclidean')
            knn_model.fit(features_matrix_sparse)
        
            # Transform user input into TF-IDF features
            user_features = vectorizer.transform([user_input])
        
            # Convert user features to sparse format
            user_features_sparse = sp.csr_matrix(user_features)
        
            # Find nearest neighbors using KNN
            distances, indices = knn_model.kneighbors(user_features_sparse)
        
            # Get recommended hotels
            recommended_hotels = df['name'].iloc[indices[0]].tolist()
        
            return recommended_hotels
        
        # Get hotel recommendations based on user input
        recommended_hotels = get_hotel_recommendations(user_input)
        
        # Prepare response
        response_data = {"recommended_hotels": recommended_hotels}
        
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
        self.send_header("Access-Control-Allow-Origin", "*")
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
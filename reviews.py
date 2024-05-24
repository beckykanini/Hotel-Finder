import json
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read data from the hotel dataset
df = pd.read_csv("C:/Users/Rebecca/Trip Advisor Dataset/Reviews/Hotel_Features_Dataset.csv")

# A dictionary to store reviews, ideally this should be a database in production
reviews_data = {}

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        parsed_data = json.loads(post_data)
        logging.info(f"Parsed data: {parsed_data}")

        if self.path == "/get_hotels":
            # Extract user input from the parsed data
            location_input = parsed_data.get("location_input", "")
            logging.info(f"Location Input: {location_input}")

            # Function to filter and collect the top 10 hotels with a rating of 5
            def get_top_rated_hotels(location_input, top_n=10, rating_threshold=5):
                # Convert the location input to lowercase for case-insensitive matching
                location_input = location_input.lower()

                # Filter hotels by location and rating threshold
                df_filtered = df[(df['country'].str.lower() == location_input) & (df['rating'] == rating_threshold)]

                # Check if any hotels are found
                if df_filtered.empty:
                    return "No hotels found in the specified location with the given rating."

                # Sort the hotels by rating in descending order and get the top N hotels
                top_rated_hotels = df_filtered.sort_values(by='rating', ascending=False).head(top_n)

                return top_rated_hotels

            # Get top rated hotels
            top_hotels = get_top_rated_hotels(location_input)

            # Prepare the response data
            if isinstance(top_hotels, str):
                response_data = {
                    "message": top_hotels
                }
            else:
                recommended_hotels = []
                for _, row in top_hotels.iterrows():
                    hotel_name = row['name']
                    if hotel_name not in reviews_data:
                        reviews_data[hotel_name] = []

                    recommended_hotels.append({
                        "name": hotel_name,
                        "rating": row['rating'],
                        "country": row['country'],
                        "google_search_link": f"https://www.google.com/search?q={hotel_name} {row['country']}",
                        "reviews": reviews_data[hotel_name]  # Include reviews
                    })
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

        elif self.path == "/submit_review":
            hotel_name = parsed_data.get("hotel_name")
            user_name = parsed_data.get("user_name")
            user_review = parsed_data.get("user_review")
            user_rating = parsed_data.get("user_rating")

            if hotel_name and user_name and user_review and user_rating:
                if hotel_name not in reviews_data:
                    reviews_data[hotel_name] = []

                reviews_data[hotel_name].append({
                    "user_name": user_name,
                    "user_review": user_review,
                    "user_rating": user_rating
                })

                response_data = {"message": "Review submitted successfully"}
            else:
                response_data = {"message": "Missing fields in the review submission"}

            # Send response
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
    logging.info(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()

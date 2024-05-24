#collaborative filtering
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import json

# Load the dataset
data = pd.read_csv("C:/Users/Rebecca/feature_engineered.csv")
data.drop("Unnamed: 0", axis=1, inplace=True)

print("Number of items in the dataset:", len(data))

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        parsed_data = json.loads(post_data)
        print("Parsed data: ", parsed_data)
        
        # Extract user input from the parsed data
        user_input = parsed_data.get("user_input", "")
        
        print("User input:", user_input)
        
        # Function to map hotel name to UUID
        def map_hotel_name_to_uuid(user_input):
            matching_hotels = data[data['name'] == user_input]['Hotel_UUID']
            print("Matching hotels:", matching_hotels)
            if not matching_hotels.empty:
                return matching_hotels.iloc[0]
            else:
                return None

        def get_recommendations(user_input):
            # Map hotel name to hotel UUID
            hotel_uuid = map_hotel_name_to_uuid(user_input)
            print("Hotel UUID:", hotel_uuid)

            if hotel_uuid is not None:
                # Create the pivot table
                data_pivot = data.pivot_table(index='Hotel_UUID', values='sentiment_scores')

                # Create the model
                model = NearestNeighbors(algorithm='brute', metric='euclidean')
                model.fit(data_pivot.values)

                # Getting the distance and indices
                query_index = data_pivot.index.get_loc(hotel_uuid)
                distances, indices = model.kneighbors(data_pivot.iloc[query_index,:].values.reshape(1,-1), n_neighbors=5)

                # Store recommendations in a list
                recommendations = []

                # Print the nearest hotels
                for i in range(1, len(distances.flatten())):
                    recommended_hotel_uuid = data_pivot.iloc[indices.flatten()[i]].name
                    location = data[data['Hotel_UUID'] == recommended_hotel_uuid]['country'].values[0]
                    recommended_hotel_name = data[data['Hotel_UUID'] == recommended_hotel_uuid]['name'].values[0]
                    rating = data_pivot.iloc[indices.flatten()[i]]['sentiment_scores']
                    recommendations.append(f'{i}: {recommended_hotel_name}, {location}, {rating}')

                return recommendations
            else:
                return ["Hotel not found in the dataset."]
        
        # Get hotel recommendations based on user input
        recommendations = get_recommendations(user_input)
        print("Recommendations:", recommendations)
        
        # Prepare response
        response_data = {"recommendations": recommendations}
        
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
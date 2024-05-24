import requests

# Function to search for nearest relevant airports based on coordinates
def search_nearest_airports(latitude, longitude):
    # Replace 'YOUR_API_KEY' with your actual Amadeus API key
    api_key = 'w8aWTldvWECSdgqpORB0BxH8xRPOGLYf'
    api_secret = 'T7zTSHirEkYGh7sI'
    api_url = f'https://test.api.amadeus.com/v1/reference-data/locations/airports?latitude={latitude}&longitude={longitude}'

    # Parameters for the API request
    params = {}

    # Headers for the API request
    headers = {
        'Authorization': f'Bearer {api_key}:{api_secret}'
    }

    # Make HTTP GET request to Amadeus API
    response = requests.get(api_url, params=params, headers=headers)

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        # Extract airport data from response
        airports = data.get('data', [])
        # Display or process the search results as needed
        print(airports)
    else:
        print(f"Error: {response.status_code} - {response.reason}")

# Example usage
user_latitude = '49.0000'  # Replace with actual latitude
user_longitude = '2.55'     # Replace with actual longitude
search_nearest_airports(user_latitude, user_longitude)

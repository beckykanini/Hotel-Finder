import requests


def get_flights(latitude, longitude):
    # Replace 'YOUR_CLIENT_ID' and 'YOUR_CLIENT_SECRET' with your actual Amadeus API credentials
    client_id = 'w8aWTldvWECSdgqpORB0BxH8xRPOGLYf'
    client_secret = 'T7zTSHirEkYGh7sI'
    api_url = 'https://test.api.amadeus.com/v1/reference-data/locations'

    # Parameters for the API request
    params = {
        'subType': 'AIRPORT,CITY',
        'latitude': latitude,
        'longitude': longitude
    }

    # Data for obtaining access token
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    # Get access token from Amadeus
    token_url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
    token_response = requests.post(token_url, data=data)

    if token_response.status_code == 200:
        access_token = token_response.json().get('access_token')

        # Headers for the API request
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        # Make HTTP GET request to Amadeus API
        response = requests.get(api_url, params=params, headers=headers)

        # Check if request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            # Extract airport city data from response
            results = data.get('data', [])
            # Display or process the search results as needed
            print(results)
            return results  # Return the results
        else:
            print(f"Error: {response.status_code} - {response.reason}")
    else:
        print(f"Error obtaining access token: {token_response.status_code} - {token_response.reason}")

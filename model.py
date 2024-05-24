#combined together
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import scipy.sparse as sp

# Sample hotel dataset

df = pd.read_csv("C:/Users/Rebecca/Trip Advisor Dataset/Reviews/Hotel_Features_Dataset.csv")

# Preprocess text data
def preprocess_text(text):
    if isinstance(text, str):
        return text.lower()
    else:
        return ''

# Concatenate features and handle missing values
df['combined_features'] = df['country'].fillna('') + ' ' + df['amenities'].fillna('') + ' ' + df['rooms'].fillna('') + ' ' + df['types'].fillna('')   
    
# Function to get hotel recommendations based on combined amenities
def get_hotel_recommendations(userInput):
    # Preprocess user input
    user_input = preprocess_text(userInput)

    # Initialize TF-IDF Vectorizer with sparse format
    vectorizer = TfidfVectorizer()
    features_matrix = vectorizer.fit_transform(df['combined_features'])

    # Convert TF-IDF matrix to sparse format
    features_matrix_sparse = sp.csr_matrix(features_matrix)

    # Train KNN model
    knn_model = NearestNeighbors(n_neighbors=3, algorithm='brute', metric='cosine')
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


# recommended_hotels = get_hotel_recommendations(userInput)
# print("Recommended hotels based on combined amenities:")
# for hotel in recommended_hotels:
#     print("- " + hotel)
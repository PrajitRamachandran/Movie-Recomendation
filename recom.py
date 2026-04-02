import numpy as np
import pandas as pd
import difflib
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ Load dataset (relative path for deployment)
movies_data = pd.read_csv('movies.csv')

# ✅ Select relevant features
selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']

# ✅ Fill missing values
for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna('')

# ✅ Combine features
combined_features = (
    movies_data['genres'] + ' ' +
    movies_data['keywords'] + ' ' +
    movies_data['tagline'] + ' ' +
    movies_data['cast'] + ' ' +
    movies_data['director']
)

# ✅ Convert text to vectors
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)

# ✅ Compute similarity matrix ONCE
similarity = cosine_similarity(feature_vectors)

# ✅ OMDb API Key
API_KEY = "7cb1263"

# ✅ Cache to avoid repeated API calls (VERY IMPORTANT)
poster_cache = {}


def get_movie_poster(title):
    # Return from cache if already fetched
    if title in poster_cache:
        return poster_cache[title]

    try:
        url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("Poster") and data["Poster"] != "N/A":
            poster_url = data["Poster"]
        else:
            poster_url = "https://via.placeholder.com/300x450?text=No+Image"

    except Exception:
        poster_url = "https://via.placeholder.com/300x450?text=Error"

    # Store in cache
    poster_cache[title] = poster_url
    return poster_url


# 🚀 MAIN FUNCTION
def recommend(movie_name, top_n=10):
    list_of_all_titles = movies_data['title'].tolist()

    # Find closest match
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

    if not find_close_match:
        return []

    close_match = find_close_match[0]

    # Get index of movie
    index_of_the_movie = movies_data[movies_data.title == close_match].index[0]

    # Get similarity scores
    similarity_score = list(enumerate(similarity[index_of_the_movie]))

    # Sort movies
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    results = []
    i = 1

    for movie in sorted_similar_movies:
        index = movie[0]
        title = movies_data.iloc[index]['title']

        if i <= top_n:
            poster = get_movie_poster(title)

            results.append({
                "title": title,
                "poster": poster
            })

            i += 1

    return results
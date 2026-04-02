# Movie Recommendation System

## Overview
This project is a content-based movie recommendation web app built with Flask and scikit-learn. A user enters a movie title, and the system suggests similar movies by comparing text features such as genres, keywords, tagline, cast, and director.

## Tech Stack
- Python
- Flask
- Pandas for CSV loading and preprocessing
- NumPy
- `difflib` for approximate title matching
- scikit-learn `TfidfVectorizer` for text vectorization
- scikit-learn `cosine_similarity` for recommendation scoring
- `requests` for poster fetching
- OMDb API for movie posters
- HTML, CSS, and Jinja2 templates
- Google Fonts

## Tools And Data Used
- Local dataset file: `movies.csv`
- External poster source: `http://www.omdbapi.com/`
- In-memory poster cache using a Python dictionary

## Recommendation Logic
### 1. Dataset loading
At import time, the app loads `movies.csv` into a Pandas DataFrame.

### 2. Feature selection
The recommender uses these text columns:
- `genres`
- `keywords`
- `tagline`
- `cast`
- `director`

Missing values in those columns are replaced with empty strings.

### 3. Feature engineering
All selected text fields are concatenated into one combined text string per movie. This creates a single content profile for each title.

### 4. Vectorization
The combined text is transformed into TF-IDF vectors using `TfidfVectorizer()`. This converts each movie into a numerical feature representation based on its descriptive terms.

### 5. Similarity computation
The code calculates a cosine-similarity matrix once when the module loads. That means recommendations are fast during requests because the expensive matrix computation is already done.

### 6. Query matching
When a user submits a movie name:
- the input title is matched against all movie titles using `difflib.get_close_matches`
- the closest matching title in the dataset is selected
- if no close match is found, the app returns an empty result list

### 7. Result generation
The app sorts movies by similarity score and returns the top matches. For each result, it also tries to fetch a poster from the OMDb API and stores the poster URL in an in-memory cache to avoid repeated API requests for the same movie.

## Project Structure
```text
Movie Recomendation/
  README.md
  app.py
  recom.py
  movies.csv
  static/
    style.css
  templates/
    index.html
```

## Important Files
- `app.py`: Flask routes and form handling
- `recom.py`: dataset loading, TF-IDF pipeline, similarity scoring, poster fetching, and final recommendation output
- `movies.csv`: source dataset used for content-based matching
- `templates/index.html`: user interface for entering a movie and showing results
- `static/style.css`: premium-themed styling for the recommendation page

## How To Run
```bash
cd "Movie Recomendation"
pip install flask pandas numpy scikit-learn requests
python app.py
```

Then open `http://127.0.0.1:5000`.

## Current Behavior Notes
- Recommendations are generated locally from the CSV dataset; only poster images depend on the internet.
- Poster URLs are fetched from OMDb using the API key currently stored in `recom.py`.
- If OMDb does not return a poster or the request fails, the app falls back to a placeholder image.
- The current ranking logic does not explicitly remove the queried movie from the recommendation list, so the searched movie can appear among the returned results.

## Summary
This project demonstrates a complete content-based recommender workflow: CSV preprocessing, text-feature fusion, TF-IDF vectorization, cosine-similarity ranking, fuzzy title matching, and Flask-based result rendering with live poster fetching.

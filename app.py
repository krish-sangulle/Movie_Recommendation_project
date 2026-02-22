from flask import Flask, render_template, request, jsonify
import pandas as pd
import ast
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    print("TMDB API Key not found. Posters will not load.")


# LOAD DATA
movies = pd.read_csv("dataset/tmdb_5000_movies.csv")
credits = pd.read_csv("dataset/tmdb_5000_credits.csv")

movies = movies.merge(credits, on="title")

movies = movies[[
    "title",
    "overview",
    "genres",
    "keywords",
    "cast",
    "crew",
    "release_date",
    "vote_average",
    "runtime"
]]

movies.fillna("", inplace=True)


# CLEAN JSON COLUMNS
def convert(text):
    result = []
    for i in ast.literal_eval(text):
        result.append(i["name"])
    return result

def fetch_director(text):
    for i in ast.literal_eval(text):
        if i["job"] == "Director":
            return i["name"]
    return ""

movies["genres"] = movies["genres"].apply(convert)
movies["keywords"] = movies["keywords"].apply(convert)
movies["cast"] = movies["cast"].apply(lambda x: convert(x)[:3])
movies["director"] = movies["crew"].apply(fetch_director)

movies["combined"] = (
    movies["overview"] + " " +
    movies["genres"].astype(str) + " " +
    movies["keywords"].astype(str) + " " +
    movies["cast"].astype(str) + " " +
    movies["director"]
)


# VECTORIZE
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
vectors = vectorizer.fit_transform(movies["combined"])

similarity = cosine_similarity(vectors)

# FETCH POSTER FROM TMDB
poster_cache = {}
def fetch_poster(movie_title):
    if movie_title in poster_cache:
        return poster_cache[movie_title]

    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
    response = requests.get(url)
    data = response.json()

    if data["results"]:
        poster_path = data["results"][0]["poster_path"]
        if poster_path:
            result = "https://image.tmdb.org/t/p/w500" + poster_path
            poster_cache[movie_title] = result
            return result

    return "https://via.placeholder.com/500x750?text=No+Image"


# RECOMMEND FUNCTION
def recommend(movie):
    if movie not in movies["title"].values:
        return []

    idx = movies[movies["title"] == movie].index[0]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:7]

    recommendations = []

    for i in scores:
        row = movies.iloc[i[0]]
        title = row.title
        poster = fetch_poster(title)

        # Safely extract fields from the dataset row with sensible fallbacks
        overview = row.get('overview', '') if hasattr(row, 'get') else row.overview if 'overview' in row.index else ''
        release_date = ''
        try:
            release_date = row.release_date if 'release_date' in row.index else ''
        except Exception:
            release_date = ''
        year = release_date[:4] if release_date else ''
        vote_average = row.vote_average if 'vote_average' in row.index else row.get('vote_average', '') if hasattr(row, 'get') else ''
        runtime = row.runtime if 'runtime' in row.index else None
        genres = row.genres if 'genres' in row.index else []

        recommendations.append({
            "title": title,
            "poster": poster,
            "overview": overview,
            "release_date": release_date,
            "year": year,
            "vote_average": vote_average,
            "runtime": runtime,
            "genres": genres,
        })

    return recommendations


# ROUTES
@app.route("/")
def home():
    titles = movies["title"].values
    return render_template("index.html", titles=titles)

@app.route("/movies")
def get_movies():
    return jsonify(movies["title"].tolist())

@app.route("/recommend", methods=["POST"])
def get_recommendation():
    data = request.json
    movie = data.get("title")
    return jsonify(recommend(movie))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
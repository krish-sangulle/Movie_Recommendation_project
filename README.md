# Movie Recommendation App

A content-based movie recommendation web app built with Flask, scikit-learn, and the TMDB API.

## Features

- Search for any movie from the TMDB 5000 dataset
- Get 6 content-based recommendations with posters, ratings, and overviews
- Responsive UI with movie details (genre, runtime, release year)

## Requirements

- Python 3.11+
- A [TMDB API key](https://www.themoviedb.org/settings/api)

## Dataset

The large CSV dataset files (`tmdb_5000_movies.csv` and `tmdb_5000_credits.csv`) are **not included** in this repository to keep it small and deployable on free hosting platforms.

### Option 1 – Download locally (for local development)

1. Download the [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) from Kaggle.
2. Place `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` inside the `dataset/` folder.

### Option 2 – Load from a remote URL (for cloud deployment)

Set the `MOVIES_CSV_URL` and `CREDITS_CSV_URL` environment variables to point to publicly accessible raw CSV URLs (e.g. a GitHub release asset, an S3 bucket, or a direct download link):

```bash
MOVIES_CSV_URL=https://example.com/tmdb_5000_movies.csv
CREDITS_CSV_URL=https://example.com/tmdb_5000_credits.csv
```

The app downloads the files at startup when no local copies are found.

## Local Development Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/krish-sangulle/Movie_Recommendation_project.git
   cd Movie_Recommendation_project
   ```

2. **Create a virtual environment and install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   ```bash
   cp .env.example .env
   # Edit .env and set TMDB_API_KEY (and optionally the CSV URLs)
   ```

4. **Add the dataset** (see [Dataset](#dataset) section above)

5. **Run the app**

   ```bash
   flask run
   ```

   Open <http://localhost:5000> in your browser.

## Deploying on Free Hosting Platforms

All three platforms below work with the same `requirements.txt` and expect the
`TMDB_API_KEY` (and optionally the CSV URL) environment variables to be set.

### Render

1. Create a new **Web Service** and connect your GitHub repository.
2. Set **Build Command**: `pip install -r requirements.txt`
3. Set **Start Command**: `gunicorn app:app`
4. Add environment variables in the Render dashboard:
   - `TMDB_API_KEY` = your key
   - `MOVIES_CSV_URL` = public URL to `tmdb_5000_movies.csv`
   - `CREDITS_CSV_URL` = public URL to `tmdb_5000_credits.csv`

### Railway

1. Create a new project and connect your GitHub repository.
2. Railway auto-detects Python – no build command needed.
3. Set **Start Command**: `gunicorn app:app`
4. Add the same environment variables in the Railway dashboard.

### PythonAnywhere

1. Create a new Web App using the **Flask** framework and Python 3.11.
2. Upload (or `git clone`) the project into your home directory.
3. In the **Files** tab, create a `.env` file with your `TMDB_API_KEY` and CSV URLs.
4. In the **Web** tab, set the WSGI file to point at `app:app`.

## Environment Variables

| Variable         | Required | Default     | Description                                    |
|------------------|----------|-------------|------------------------------------------------|
| `TMDB_API_KEY`   | Yes      | —           | API key from themoviedb.org                    |
| `FLASK_ENV`      | No       | `production`| `development` enables debug/reloader           |
| `PORT`           | No       | `5000`      | Port the server listens on                     |
| `MOVIES_CSV_URL` | No       | —           | Remote URL for `tmdb_5000_movies.csv`          |
| `CREDITS_CSV_URL`| No       | —           | Remote URL for `tmdb_5000_credits.csv`         |

## API Endpoints

| Method | Path         | Description                                   |
|--------|--------------|-----------------------------------------------|
| GET    | `/`          | Home page with movie search                   |
| GET    | `/movies`    | JSON list of all available movie titles       |
| POST   | `/recommend` | Returns 6 recommendations for a given title   |

**POST `/recommend` body:**

```json
{ "title": "The Dark Knight" }
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes and open a pull request

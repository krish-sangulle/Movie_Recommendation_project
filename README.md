# Movie Recommendation App

A content-based movie recommendation web app built with Flask, scikit-learn, and the TMDB API.

## Features

- Search for any movie from the TMDB 5000 dataset
- Get 6 content-based recommendations with posters, ratings, and overviews
- Responsive UI with movie details (genre, runtime, release year)

## Requirements

- Python 3.11+
- A [TMDB API key](https://www.themoviedb.org/settings/api)

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
   # Edit .env and set TMDB_API_KEY
   ```

4. **Run the app**

   ```bash
   flask run
   ```

   Open <http://localhost:5000> in your browser.

## Docker Deployment

### Build and run with Docker

```bash
docker build -t movie-recommendation .
docker run -p 5000:5000 -e TMDB_API_KEY=your_key movie-recommendation
```

### Docker Compose (recommended for development)

```bash
cp .env.example .env   # fill in TMDB_API_KEY
docker-compose up
```

## Environment Variables

| Variable       | Required | Default       | Description                          |
|----------------|----------|---------------|--------------------------------------|
| `TMDB_API_KEY` | Yes      | —             | API key from themoviedb.org          |
| `FLASK_ENV`    | No       | `production`  | `development` enables debug/reloader |
| `PORT`         | No       | `5000`        | Port the server listens on           |

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

## Heroku Deployment

The `Procfile` is included for Heroku. Set `TMDB_API_KEY` as a config var:

```bash
heroku config:set TMDB_API_KEY=your_key
git push heroku main
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes and open a pull request

import pandas as pd
from db import get_db
from pymongo import MongoClient

def import_movies():
    db = get_db()

    # Load movie data from CSV file
    movies = pd.read_csv('../../ml-100k/u.item',
                         sep='|',
                         names=['movieId', 'title', 'release_date', 'video_release_date',
                                'IMDb_URL', 'unknown', 'Action', 'Adventure', 'Animation',
                                'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
                                'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
                                'Thriller', 'War', 'Western'],
                         encoding='latin-1')

    # Columns representing movie genres
    genre_columns = ['unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
                     'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
                     'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

    # Extract genres for each movie based on binary columns
    def extract_genres(row):
        genres = [genre for genre in genre_columns if row[genre] == 1]
        return genres

    movies['genres'] = movies.apply(extract_genres, axis=1)
    movies = movies[['movieId', 'title', 'release_date', 'genres']]

    # Handle missing release dates
    movies['release_date'] = movies['release_date'].fillna(None)

    # Load ratings data from CSV file
    ratings = pd.read_csv('../../ml-100k/u.data', sep='\t',
                          names=['userId', 'movieId', 'rating', 'timestamp'])

    # Convert movies DataFrame to dictionary records for MongoDB
    movies_docs = movies.to_dict('records')
    db.movies.insert_many(movies_docs)

    # Convert ratings DataFrame to dictionary records for MongoDB
    ratings_docs = ratings.to_dict('records')
    db.ratings.insert_many(ratings_docs)

import_movies()

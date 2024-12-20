import pandas as pd
from db import get_db
from pymongo import MongoClient

def import_movies():
    db = get_db()

    movies = pd.read_csv('../../ml-100k/u.item',
                         sep='|',
                         names=['movieId', 'title', 'release_date', 'video_release_date',
                                'IMDb_URL', 'unknown', 'Action', 'Adventure', 'Animation',
                                'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
                                'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
                                'Thriller', 'War', 'Western'],
                        encoding='latin-1')
    
    genre_columns = ['unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
                     'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
                     'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    
    def extract_genres(row):
        genres = []
        for genre in genre_columns:
            if row[genre] == 1:
                genres.append(genre)
        return genres
    
    movies['genres'] = movies.apply(extract_genres, axis=1)
    movies = movies[['movieId', 'title', 'release_date', 'genres']]

    movies['release_date'] = movies['release_date'].fillna(None)

    ratings = pd.read_csv('../../ml-100k/u.data', sep='\t',
                          names=['userId', 'movieId', 'rating', 'timestamp'])
    
    movies_docs = movies.to_dict('records')
    db.movies.insert_many(movies_docs)

    ratings_docs = ratings.to_dict('records')
    db.ratings.insert_many(ratings_docs)

import_movies()

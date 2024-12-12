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
    
    ratings = pd.read_csv('../../ml-100k/u.data', sep='\t',
                          names=['userId', 'movieId', 'rating', 'timestamp'])
    
    movies_docs = movies.to_dict('records')
    db.movies.insert_many(movies_docs)

    ratings_docs = ratings.to_dict('records')
    db.ratings.insert_many(ratings_docs)

import_movies()

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import numpy as np
from db import get_db

def load_data():
    db = get_db()
    movies = list(db.movies.find({}, {'_id': 0}))
    ratings = list(db.ratings.find({}, {'_id': 0}))

    movies_df = pd.DataFrame(movies)
    ratings_df = pd.DataFrame(ratings)

    return movies_df, ratings_df


def content_based_recommendations(movie_id, movies_df):
    movies_df['genres combined'] = movies_df['genres'].apply(lambda x:' '.join(x))

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_df['genres_combined'])

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(movies_df.index, index = movies_df['movieId'])

    idx = indices[movie_id]

    sim_score= list(enumerate(cosine_sim[idx]))

    movie_indices = [i[0] for i in sim_score[1:11]]

    return movies_df.iloc[movie_indices][['movieId', 'title', 'genres']]
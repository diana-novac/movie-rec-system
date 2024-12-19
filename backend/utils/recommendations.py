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

def collaborative_recommendations(user_id, ratings_df, movies_df):
    user_movie_matrix = ratings_df.pivot(index='userId', columns='movieId', values='rating').fillna(0)

    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(user_movie_matrix)

    user_ratings = user_movie_matrix.loc[user_id].values.reshape(1, -1)

    distances, indices = knn.kneighbors(user_ratings, n_neighbors=10)

    similar_users = user_movie_matrix.iloc[indices[0]]
    similar_movies = similar_users.mean(axis=0).sort_values(ascending=False)

    valid_movies = similar_movies.index[similar_movies.index.isin(movies_df['movieId'])]
    recommended_movie_ids = valid_movies[:10]

    return movies_df[movies_df['movieId'].isin(recommended_movie_ids)][['movieId', 'title', 'genres']]

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

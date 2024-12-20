import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from utils.db import get_db

def load_data():
    db = get_db()
    movies = list(db.movies.find({}, {'_id': 0}))
    ratings = list(db.ratings.find({}, {'_id': 0}))

    movies_df = pd.DataFrame(movies)
    ratings_df = pd.DataFrame(ratings)

    return movies_df, ratings_df

def collaborative_recommendations(user_id, ratings_df, movies_df):
    ratings_df = ratings_df.drop_duplicates(subset=['userId', 'movieId']).dropna(subset=['userId', 'movieId', 'rating'])

    ratings_df['rating'] = pd.to_numeric(ratings_df['rating'], errors='coerce')
    
    user_movie_matrix = ratings_df.pivot(index='userId', columns='movieId', values='rating').fillna(0)

    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(user_movie_matrix)

    if user_id not in user_movie_matrix.index:
        return pd.DataFrame()

    user_ratings = user_movie_matrix.loc[user_id].values.reshape(1, -1)
    distances, indices = knn.kneighbors(user_ratings, n_neighbors=10)

    similar_users = user_movie_matrix.iloc[indices[0]]
    similar_movies = similar_users.mean(axis=0).sort_values(ascending=False)

    valid_movies = similar_movies.index[similar_movies.index.isin(movies_df['movieId'])]
    recommended_movie_ids = valid_movies[:10]

    return movies_df[movies_df['movieId'].isin(recommended_movie_ids)][['movieId', 'title', 'genres']]

def content_based_recommendations(movie_id, movies_df):
    movies_df['genres_combined'] = movies_df['genres'].apply(lambda x: ' '.join(x))

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_df['genres_combined'])

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(movies_df.index, index=movies_df['movieId'])
    if movie_id not in indices:
        return pd.DataFrame()

    idx = indices[movie_id]
    sim_score = list(enumerate(cosine_sim[idx]))
    sim_score = sorted(sim_score, key=lambda x: x[1], reverse=True)

    movie_indices = [i[0] for i in sim_score[1:11]]

    return movies_df.iloc[movie_indices][['movieId', 'title', 'genres']]

def hybrid_recommendations(user_id, movie_id, movies_df, ratings_df):
    content_recs = content_based_recommendations(movie_id, movies_df)

    collaborative_recs = collaborative_recommendations(user_id, ratings_df, movies_df)
    hybrid_recs = pd.concat([content_recs, collaborative_recs]).drop_duplicates('movieId')

    return hybrid_recs.head(10)
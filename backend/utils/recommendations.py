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
    # Prepare the user-movie rating matrix
    ratings_df = ratings_df.drop_duplicates(subset=['userId', 'movieId']).dropna(subset=['userId', 'movieId', 'rating'])
    ratings_df['rating'] = pd.to_numeric(ratings_df['rating'], errors='coerce')
    user_movie_matrix = ratings_df.pivot(index='userId', columns='movieId', values='rating').fillna(0)

    # Train a KNN model for collaborative filtering
    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(user_movie_matrix)

    if user_id not in user_movie_matrix.index:
        return pd.DataFrame()

    # Find similar users and their movie preferences
    user_ratings = user_movie_matrix.loc[user_id].values.reshape(1, -1)
    distances, indices = knn.kneighbors(user_ratings, n_neighbors=10)
    similar_users = user_movie_matrix.iloc[indices[0]]
    similar_movies = similar_users.mean(axis=0).sort_values(ascending=False)

    # Filter recommendations to valid movie IDs
    valid_movies = similar_movies.index[similar_movies.index.isin(movies_df['movieId'])]
    recommended_movie_ids = valid_movies[:1000]

    return movies_df[movies_df['movieId'].isin(recommended_movie_ids)][['movieId', 'title', 'genres']]

def content_based_recommendations(movie_id, movies_df):
    # Combine genres into a single string for TF-IDF
    movies_df['genres_combined'] = movies_df['genres'].apply(lambda x: ' '.join(x))

    # Compute cosine similarity on TF-IDF vectors
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_df['genres_combined'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Get indices for the target movie and similar movies
    indices = pd.Series(movies_df.index, index=movies_df['movieId'])
    if movie_id not in indices:
        return pd.DataFrame()

    idx = indices[movie_id]
    sim_score = list(enumerate(cosine_sim[idx]))
    sim_score = sorted(sim_score, key=lambda x: x[1], reverse=True)

    # Select top 10 most similar movies
    movie_indices = [i[0] for i in sim_score[1:1001]]

    return movies_df.iloc[movie_indices][['movieId', 'title', 'genres']]

def hybrid_recommendations(user_id, movie_id, movies_df, ratings_df, content_weight=0.6, collaborative_weight=0.4, diversity_penalty=0.3):
    # Get individual recommendations
    content_recs = content_based_recommendations(movie_id, movies_df)
    collaborative_recs = collaborative_recommendations(user_id, ratings_df, movies_df)

    # Merge recommendations and remove movies already rated by the user
    combined_recs = pd.concat([content_recs, collaborative_recs]).drop_duplicates('movieId')
    user_rated_movie_ids = [rating['movieId'] for rating in ratings_df[ratings_df['userId'] == user_id].to_dict('records')]
    combined_recs = combined_recs[~combined_recs['movieId'].isin(user_rated_movie_ids)]

    combined_recs['score'] = 0

    # Add weights for content-based and collaborative scores
    for i, row in combined_recs.iterrows():
        if row['movieId'] in content_recs['movieId'].values:
            combined_recs.at[i, 'score'] += content_weight
        if row['movieId'] in collaborative_recs['movieId'].values:
            combined_recs.at[i, 'score'] += collaborative_weight

    # Add diversity by prioritizing movies with unique genres
    genre_penalty = combined_recs['genres'].apply(lambda genres: len(set(genres)))
    combined_recs['score'] -= diversity_penalty * genre_penalty

    combined_recs['score'] = (combined_recs['score'] - combined_recs['score'].min()) / (combined_recs['score'].max() - combined_recs['score'].min())

    return combined_recs.sort_values(by='score', ascending=False).head(12)[['movieId', 'title', 'genres', 'score']]

from flask import Blueprint, jsonify, request
from flask import Response, json
from utils.db import get_db
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.recommendations import load_data, hybrid_recommendations
import pandas as pd

movies_blueprint = Blueprint('movies', __name__)

@movies_blueprint.route('/get-all-movies', methods=['GET'])
def list_movies():
    db = get_db()
    movies = list(db.movies.find({}, {'_id': 0}))
    return jsonify(movies), 200

@movies_blueprint.route('/search-movie', methods=['GET'])
def search_movies():
    db = get_db()
    title = request.args.get('title')
    
    if not title:
        return jsonify({'message': 'Invalid request'}), 400
    
    query = {'title': {'$regex': title, '$options': 'i'}}
    movies = list(db.movies.find(query, {'_id': 0}))

    return jsonify(movies), 200

@movies_blueprint.route('/filter-genre', methods=['GET'])
def filter_genre():
    db = get_db()
    genre = request.args.get('genre')

    if not genre:
        return jsonify({'message': 'Invalid request'}), 400
    query = {'genres':genre}
    movies = list(db.movies.find(query, {'_id': 0}))

    return jsonify(movies), 200


@movies_blueprint.route('/rate', methods=['POST'])
@jwt_required()
def rate_movie():
    db = get_db()
    username = get_jwt_identity()
    data = request.get_json()

    movie_id = data.get('movie_id')
    rating = data.get('rating')

    if movie_id is None:
        return jsonify({'message': 'Invalid movie_id'}), 400

    db.users.update_one(
        {'username': username},
        {'$pull': {'ratings': {'movie_id': movie_id}}}
    )

    db.users.update_one(
        {'username': username},
        {'$push': {'ratings': {'movie_id': movie_id, 'rating': rating}}}
    )

    db.ratings.update_one(
        {'userId': username, 'movieId': movie_id},
        {'$set': {'rating': rating}},
        upsert=True
    )

    return jsonify({'message': 'Rating added/updated successfully!'}), 200

@movies_blueprint.route('/user/ratings', methods=['GET'])
@jwt_required()
def get_user_ratings():
    db = get_db()
    username = get_jwt_identity()

    user = db.users.find_one(
        {'username': username},
        {'_id': 0, 'ratings': 1}
    )

    if not user or 'ratings' not in user:
        return jsonify({'ratings': []}), 200
    
    return jsonify({'ratings': user['ratings']}), 200

@movies_blueprint.route('/recommend-hybrid', methods=['GET'])
@jwt_required()
def recommend_hybrid():
    db = get_db()
    username = get_jwt_identity()

    user = db.users.find_one({'username': username}, {'_id': 0, 'ratings': 1})
    if not user:
        return jsonify({'recommendations': []}), 200

    user_ratings = user['ratings']

    user_ratings = [r for r in user_ratings if r['movie_id'] is not None]

    movies_df, ratings_df = load_data()

    for rating in user_ratings:
        new_rating = {
            'userId': username,
            'movieId': rating['movie_id'],
            'rating': rating['rating'],
            'timestamp': None
        }
        ratings_df = pd.concat([ratings_df, pd.DataFrame([new_rating])], ignore_index=True)

    high_rated_movies = [r['movie_id'] for r in user_ratings if r['rating'] >= 4]

    if not high_rated_movies:
        return jsonify({'recommendations': []}), 200

    movie_id = high_rated_movies[0]

    recommendations = hybrid_recommendations(username, movie_id, movies_df, ratings_df)

    return jsonify({'recommendations': recommendations.to_dict(orient='records')}), 200
from flask import Blueprint, jsonify, request
from utils.db import get_db

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


@movies_blueprint.route('/recommend-content', methods = ['GET'])
@jwt_required()
def recommend_content():
    db = get_db()
    username = get_jwt_identity()

    user = db.users.find_one({'username': username}, {'_id': 0, 'ratings': 1})
    if not user or 'ratings' not in user:
        return jsonify({'recommendations': []}), 200

    high_rated_movies = [r['movie_id'] for r in user['ratings'] if r['rating'] >= 4]

    if not high_rated_movies:
        return jsonify({'recommendations': []}), 200

    genres = set()
    for movie_id in high_rated_movies:
        movie = db.movies.find_one({'movieId': movie_id}, {'_id': 0, 'genres': 1})
        if movie:
            genres.update(movie['genres'])

    recommendations = list(db.movies.find(
        {'genres': {'$in': list(genres)}},
        {'_id': 0, 'movieId': 1, 'title': 1, 'genres': 1}
    ))

    return jsonify({'recommendations': recommendations}), 200
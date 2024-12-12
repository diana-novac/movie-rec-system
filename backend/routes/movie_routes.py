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
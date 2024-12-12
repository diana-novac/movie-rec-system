from flask import Blueprint, jsonify
from utils.db import get_db

movies_blueprint = Blueprint('movies', __name__)

@movies_blueprint.route('/get-all-movies', methods=['GET'])
def list_movies():
    db = get_db()
    movies = list(db.movies.find({}, {'_id': 0}))
    return jsonify(movies), 200


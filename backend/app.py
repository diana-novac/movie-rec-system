from flask import Flask
from utils.db import get_db

from routes.auth_routes import auth_blueprint
from flask_jwt_extended import JWTManager
from routes.movie_routes import movies_blueprint

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db = get_db()

app.config['JWT_SECRET_KEY'] = 'abcdef1234567890abcdef1234567890'

jwt = JWTManager(app)

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(movies_blueprint, url_prefix='/movies')

if __name__ == '__main__':
    app.run(debug=True)

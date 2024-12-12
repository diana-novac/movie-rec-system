from werkzeug.security import generate_password_hash, check_password_hash
import re

class User:
    def __init__(self, username, email, password, ratings=None):
        self.username = username
        self.email = email
        self.password = self.hash_password(password)
        self.ratings = []

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @staticmethod
    def validate_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
    
    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "ratings": self.ratings
        }

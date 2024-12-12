from flask import Flask
from utils.db import get_db

app = Flask(__name__)
db = get_db()

@app.route('/')
def home():
    try:
        db.command("ping")
        return "Connected to MongoDB"
    except Exception as e:
        return f"Failed to connect to MongoDB: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)

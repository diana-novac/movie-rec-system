# Movie Recommender Application

### Authors:
    Barbu Antonia-Maria
    Novac Diana-Ioana

### Github Link:
https://github.com/diana-novac/movie-rec-system

## Project Overview

This project is a movie recommendation system that provides users with:
- Personalized movie recommendations based on hybrid collaborative and content-based filtering
- The ability to rate movies
- Search and filter movies by genre
- A user-friendly interface built in React

## Project Structure:
### Frontend:
```bash
src/
├── components/
│   ├── navbar.jsx             # Main navigation bar
│   ├── rate_movie_form.jsx    # Component for movie rating
├── pages/
│   ├── Homepage.jsx           # Landing page for the app
│   ├── login.jsx              # Login page for users
│   ├── register.jsx           # Registration page for new users
│   ├── movies.jsx             # Page to browse and filter movies
│   ├── recommendations.jsx    # Page to display personalized recommendations
│   ├── my_ratings.jsx         # Page to view user's movie ratings
├── App.jsx                    # Main React app entry point
├── App.css                    # Global app-specific CSS
├── index.css                  # Global styles and resets
```
### Backend:
```bash
.
├── app.py                     # Main entry point
├── models                     
│   └── user_model.py           #Defines a user structure
├── requirements.txt
├── routes
│   ├── auth_routes.py          # API routes for authentication operations
│   └── movie_routes.py         # Movie related routes
└── utils
    ├── db.py                   # MongoDB connection setup
    ├── import_movielens.py     # Script for importing the data locally
    └── recommendations.py      # Hybrid recommendation engine
```

## Technologies used
### Frontend:
- React: For the user interface
- Axios: For making requests to the backend
- CSS: Custom styles for the UI

### Backend:
- Flask: Backend framework
- MongoDB: Database for storing movies, users, ratings
- Sci-kit Learn: For the recommendation algorithm
- Pandas: For data handling

## Running the project
- You should have npm and mongodb installed
- Run the import_movielens.py script to load the movie data into your local database
- Run *pip install -r requirements.txt*
- Run the frontend with *npm run dev*
- Run the backend with *python3 app.py*

## System Overview

## 1. Data Initialization

### Loading Movies and Ratings
- **Movies Collection:**
  - Stores metadata for each movie, including:
    - `title`
    - `genres`
    - `release year`
  - Stored in a MongoDB collection named `movies`.

- **Ratings Collection:**
  - Stores user ratings for movies in a separate MongoDB collection named `ratings`.
  - Each rating includes:
    - `userId`: Links the rating to a specific user.
    - `movieId`: Identifier for the rated movie.
    - `rating`: Numerical value (e.g., 1–5).

### User Data Tracking
- **Users Collection:**
  - Contains fields for:
    - `username`
    - `password` (hashed)
    - `ratings`: A list of movies rated by the user.
  
- **Each Rating Includes:**
  - `movie_id`: Identifier for the rated movie.
  - `rating`: Numerical value of the rating.
  - `timestamp`: Optional timestamp.

### Database Connection
- **Module:** `utils/db.py`
  - Manages the connection to the MongoDB instance.
  - Provides utility functions for interacting with the `movies`, `ratings`, and `users` collections.

---

## 2. Recommendation Logic

### Collaborative Filtering
- Identifies users with similar rating patterns to the current user.
- Recommends movies based on the preferences of these similar users, using KNN algorithm.

### Content-Based Filtering
- Analyzes movie genres to find similar movies.
- Uses **TF-IDF vectorization** on genres to compute similarity scores between movies.

### Hybrid Recommendation (`recommend_hybrid`)
- Combines collaborative and content-based approaches.
- Balances both strategies using configurable weights; we chose 0.6 content weight and 0.4 collaborative weight
- Promotes variety in recommendations by reducing the impact of similar genres.
---


## 3. API Routes

### **Movie Management**
- `/movies/get-all-movies` (GET): Fetches all movies.
- `/movies/search-movie` (GET): Searches for movies by title.
- `/movies/filter-genre` (GET): Filters movies by genre.

### **User Interactions**
- `/movies/rate` (POST): Allows users to rate movies (requires JWT).
- `/movies/user/ratings` (GET): Fetches movies rated by the current user (requires JWT).

### **Recommendations**
- `/movies/recommend-hybrid` (GET): Generates personalized recommendations using a hybrid recommendation model.


### Team responsibilities
We worked together most of the time, but we split some of the tasks; for example:
- While Antonia was writing the content based recommendation logic, Diana was working on the collaborative filtering
- Antonia implemented the login route and Diana the register one
- Diana preprocessed data and wrote the rating routes, while Antonia implemented search and filter functionalities
- For the frontend, we only worked together

### Possible future enhancements
- Add advanced filtering options(release yeaar, popularity)
- Improve recommendation algorithms
- Add authentication functionalities (forgot password, email confirmation)


### Resources
https://scikit-learn.org/1.5/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
https://scikit-learn.org/dev/auto_examples/neighbors/plot_classification.html
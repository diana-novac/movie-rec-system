import { Link } from 'react-router-dom';
import { useState } from 'react';
import axios from 'axios';

const Homepage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  const handleSearch = async () => {
    if (!searchQuery) return;

    try {
      const res = await axios.get(
        `${import.meta.env.VITE_API_URL}/movies/search-movie?title=${searchQuery}`
      );
      setSearchResults(res.data);
    } catch (error) {
      console.error('Failed to search movies:', error);
    }
  };

  return (
    <div>
      <h1>Welcome to Movie Recommender</h1>
      <p>
        Discover your favorite movies and enjoy personalized recommendations
        tailored just for you!
      </p>

      <div>
        <input
          type="text"
          placeholder="Search for a movie..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      {/* Search Results */}
      {searchResults.length > 0 && (
        <div>
          <h3>Search Results:</h3>
          <ul>
            {searchResults.map((movie) => (
              <li key={movie.movieId}>
                {movie.title} - {movie.genres.join(', ')}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Quick Links */}
      <div>
        <Link to="/movies">
          <button>Explore Movies</button>
        </Link>
        <Link to="/recommendations">
          <button>Get Recommendations</button>
        </Link>
        <Link to="/filter">
          <button>Filter by Genre</button>
        </Link>
      </div>
    </div>
  );
};

export default Homepage;

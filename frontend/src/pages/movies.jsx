import { useEffect, useState } from 'react';
import axios from 'axios';

const Movies = () => {
    const [movies, setMovies] = useState([]);

    useEffect(() => {
        const fetchMovies = async () => {
            try {
                const res = await axios.get(`${import.meta.env.VITE_API_URL}/movies/get-all-movies`);
                
                const parsedData = typeof res.data === 'string' ? JSON.parse(res.data) : res.data;
                setMovies(parsedData);
            } catch (error) {
                console.error('Failed to fetch movies:', error);
            }
        };

        fetchMovies();
    }, []);

    return (
        <div>
          <h1>All Movies</h1>
          <ul>
            {Array.isArray(movies) ? (
              movies.map((movie) => (
                <li key={movie.movieId}>
                  {movie.title} - {movie.genres.join(', ')}
                </li>
              ))
            ) : (
              <p>No movies available</p>
            )}
          </ul>
        </div>
      );
      
};

export default Movies;
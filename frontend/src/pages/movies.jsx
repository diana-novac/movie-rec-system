import { useEffect, useState } from 'react';
import axios from 'axios';

const Movies = () => {
    const [movies, setMovies] = useState([]);

    useEffect(() => {
        const fetchMovies = async () => {
            try {
                const res = await axios.get(`${import.meta.env.VITE_API_URL}/movies/get-all-movies`);
                setMovies(res.data);
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
                {movies.map((movie) => (
                    <li key={movie.movieId}>
                        {movie.title} - {movie.genres.join(', ')}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Movies;
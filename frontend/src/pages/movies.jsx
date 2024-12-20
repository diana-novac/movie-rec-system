import { useEffect, useState } from 'react';
import axios from 'axios';
import RateMovieForm from '../components/rate_movie_form';
import ClipLoader from 'react-spinners/ClipLoader'; 

const Movies = () => {
    const [movies, setMovies] = useState([]);
    const [displayedMovies, setDisplayedMovies] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedGenre, setSelectedGenre] = useState('');
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const genres = [
        'unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
        'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
        'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'
    ];

    useEffect(() => {
        const fetchMovies = async () => {
            setIsLoading(true);
            try {
                const res = await axios.get(`${import.meta.env.VITE_API_URL}/movies/get-all-movies`);
                const parsedData = typeof res.data === 'string' ? JSON.parse(res.data) : res.data;
                setMovies(parsedData);
                setDisplayedMovies(parsedData.slice(0, 100));
            } catch (error) {
                console.error('Failed to fetch movies:', error);
                setMessage('Failed to fetch movies');
            } finally {
                setIsLoading(false);
            }
        };

        fetchMovies();
    }, []);

    const handleSearch = async () => {
        if (!searchQuery) {
            setDisplayedMovies(movies.slice(0, 100));
            return;
        }

        setIsLoading(true);
        try {
            const res = await axios.get(
                `${import.meta.env.VITE_API_URL}/movies/search-movie?title=${searchQuery}`
            );
            const parsedData = typeof res.data === 'string' ? JSON.parse(res.data) : res.data;
            setDisplayedMovies(parsedData);
        } catch (error) {
            console.error('Failed to search movies:', error);
            setMessage('Failed to search movies');
        } finally {
            setIsLoading(false);
        }
    };

    const handleGenreFilter = async (genre) => {
        setSelectedGenre(genre);
        setIsLoading(true);
        if (!genre) {
            setDisplayedMovies(movies.slice(0, 100));
            setIsLoading(false);
            return;
        }

        try {
            const res = await axios.get(
                `${import.meta.env.VITE_API_URL}/movies/filter-genre?genre=${genre}`
            );
            const parsedData = typeof res.data === 'string' ? JSON.parse(res.data) : res.data;
            setDisplayedMovies(parsedData);
        } catch (error) {
            console.error('Failed to filter movies by genre:', error);
            setMessage('Failed to filter movies by genre');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="container">
            <h1>All Movies</h1>
            
            <div>
                <input
                    type="text"
                    placeholder="Search for a movie..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
                <button onClick={handleSearch}>Search</button>
            </div>

            <div>
                <label htmlFor="genre-select">Filter by Genre:</label>
                <select
                    id="genre-select"
                    value={selectedGenre}
                    onChange={(e) => handleGenreFilter(e.target.value)}
                >
                    <option value="">All Genres</option>
                    {genres.map((genre) => (
                        <option key={genre} value={genre}>
                            {genre}
                        </option>
                    ))}
                </select>
            </div>

            {message && <p>{message}</p>}

            {isLoading && (
                <div className="spinner-container">
                    <ClipLoader size={50} color="#36d7b7" loading={isLoading} />
                </div>
            )}

            <ul className="movies-list">
                {Array.isArray(displayedMovies) && displayedMovies.length > 0 ? (
                    displayedMovies.map((movie) => (
                        <li key={movie.movieId}>
                            <h3>{movie.title}</h3>
                            <p>Genres: {movie.genres.join(', ')}</p>
                            <RateMovieForm
                                movieId={movie.movieId}
                                onSuccess={() => console.log(`Rating added for movie ${movie.movieId}`)}
                            />
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

import { useEffect, useState } from 'react';
import axios from 'axios';
import ClipLoader from 'react-spinners/ClipLoader';  // Importă ClipLoader
import RateMovieForm from '../components/rate_movie_form';

const Movies = () => {
    const [movies, setMovies] = useState([]);
    const [displayedMovies, setDisplayedMovies] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedGenre, setSelectedGenre] = useState('');
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);  // Adăugăm starea pentru încărcare

    const genres = [
        'unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
        'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
        'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'
    ];

    useEffect(() => {
        const fetchMovies = async () => {
            setIsLoading(true);  // Setăm la true când începe încărcarea
            try {
                const res = await axios.get(`${import.meta.env.VITE_API_URL}/movies/get-all-movies`);
                const parsedData = typeof res.data === 'string' ? JSON.parse(res.data) : res.data;
                setMovies(parsedData);
                setDisplayedMovies(parsedData.slice(0, 100)); // Afișează primele 100 filme
            } catch (error) {
                console.error('Failed to fetch movies:', error);
                setMessage('Failed to fetch movies');
            } finally {
                setIsLoading(false);  // Setăm la false când s-a terminat încărcarea
            }
        };

        fetchMovies();
    }, []);

    const handleSearch = async () => {
        if (!searchQuery) {
            // Dacă nu există căutare, afișează primele 100 filme
            setDisplayedMovies(movies.slice(0, 100));
            return;
        }

        setIsLoading(true);  // Setăm la true când începe căutarea
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
            setIsLoading(false);  // Setăm la false când s-a terminat căutarea
        }
    };

    const handleGenreFilter = async (genre) => {
        setSelectedGenre(genre);
        setIsLoading(true);  // Setăm la true când începe filtrarea
        if (!genre) {
            // Dacă nu este selectat niciun gen, afișează primele 100 filme
            setDisplayedMovies(movies.slice(0, 100));
            setIsLoading(false);  // Setăm la false dacă nu este niciun filtru
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
            setIsLoading(false);  // Setăm la false când s-a terminat filtrarea
        }
    };

    return (
        <div>
            <h1>All Movies</h1>
            
            {/* Search Bar */}
            <div>
                <input
                    type="text"
                    placeholder="Search for a movie..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
                <button onClick={handleSearch}>Search</button>
            </div>

            {/* Genre Dropdown */}
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

            {/* Spinner de încărcare */}
            {isLoading && (
                <div className="spinner-container">
                    <ClipLoader color="#3498db" loading={isLoading} size={50} />
                </div>
            )}

            {/* Movie List */}
            <ul>
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

import { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import RateMovieForm from '../components/rate_movie_form';

const Homepage = () => {
	const [searchQuery, setSearchQuery] = useState('');
	const [searchResults, setSearchResults] = useState([]);
	const [message, setMessage] = useState('');

	const handleSearch = async () => {
		if (!searchQuery) return;

		try {
			const res = await axios.get(
				`${import.meta.env.VITE_API_URL}/movies/search-movie?title=${searchQuery}`
			);
			setSearchResults(res.data);
		} catch (error) {
			console.error('Failed to search movies:', error);
			setMessage('Failed to search movies');
		}
	};

	return (
		<div className="homepage container">
			<h1 className="homepage-title">Welcome to Movie Recommender</h1>

			<div className="search-section">
				<input
					type="text"
					className="search-input"
					placeholder="Search for a movie..."
					value={searchQuery}
					onChange={(e) => setSearchQuery(e.target.value)}
				/>
				<button className="search-button" onClick={handleSearch}>Search</button>
			</div>

			<div className="buttons-section">
				<Link to="/movies">
					<button className="nav-button">Explore Movies</button>
				</Link>
				<Link to="/recommendations">
					<button className="nav-button">Get Recommendations</button>
				</Link>
			</div>

			{searchResults.length > 0 && (
				<div className="search-results">
					<h2>Search Results</h2>
					<ul>
						{searchResults.map((movie) => (
							<li key={movie.movieId} className="movie-card">
								<div>
									<h3>{movie.title}</h3>
									<p>Genres: {movie.genres.join(', ')}</p>
									<div className="rating-section">
										<RateMovieForm
											movieId={movie.movieId}
											onSuccess={setMessage}
										/>
									</div>
								</div>
							</li>
						))}
					</ul>
				</div>
			)}

			{message && <p className="message">{message}</p>}
		</div>
	);
};

export default Homepage;
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
		<div>
			<h1>Welcome to Movie Recommender</h1>
			<p>Discover your favorite movies and rate them directly!</p>

			{/* Search Section */}
			<div>
				<input
					type="text"
					placeholder="Search for a movie..."
					value={searchQuery}
					onChange={(e) => setSearchQuery(e.target.value)}
				/>
				<button onClick={handleSearch}>Search</button>
			</div>

			{/* Navigation Buttons */}
			<div>
				<Link to="/movies">
					<button>Explore Movies</button>
				</Link>
				<Link to="/recommendations">
					<button>Get Recommendations</button>
				</Link>
			</div>

			{/* Search Results */}
			{searchResults.length > 0 && (
				<div>
					<h2>Search Results</h2>
					<ul>
						{searchResults.map((movie) => (
							<li key={movie.movieId}>
								<div>
									<h3>{movie.title}</h3>
									<p>Genres: {movie.genres.join(', ')}</p>
									<RateMovieForm
										movieId={movie.movieId}
										onSuccess={() => setMessage('Rating added successfully')}
									/>
								</div>
							</li>
						))}
					</ul>
				</div>
			)}

			{message && <p>{message}</p>}
		</div>
	);
};

export default Homepage;
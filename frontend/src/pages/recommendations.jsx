import { useEffect, useState } from 'react';
import axios from 'axios';
import { ClipLoader } from 'react-spinners';
const Recommendations = () => {
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState('');

    useEffect(() => {
        const fetchRecommendations = async () => {
            const token = localStorage.getItem('token');

            if (!token) {
                setMessage('You must be logged in to view recommendations');
                setLoading(false);
                return;
            }

            try {
                const res = await axios.get(
                    `${import.meta.env.VITE_API_URL}/movies/recommend-hybrid`,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
            },
        }
        );
    setRecommendations(res.data.recommendations);
    setLoading(false);
} catch (error) {
    console.error('Failed to fetch recommendations:', error);
    setMessage('Failed to fetch recommendations');
    setLoading(false);
}
    };

fetchRecommendations();
  }, []);

return (
    <div>
        <h1>Your Recommendations</h1>
        {loading ? (
            <ClipLoader size={50} />
        ) : message ? (
            <p>{message}</p>
        ) : recommendations.length > 0 ? (
            <ul>
                {recommendations.map((movie) => (
                    <li key={movie.movieId}>
                        <h3>{movie.title}</h3>
                        <p>Genres: {movie.genres.join(', ')}</p>
                    </li>
                ))}
            </ul>
        ) : (
            <p>No recommendations available</p>
        )}
    </div>
);
};

export default Recommendations;
import { useEffect, useState } from 'react';
import axios from 'axios';
import ClipLoader from 'react-spinners/ClipLoader';

const MyRatings = () => {
    const [userRatings, setUserRatings] = useState([]);
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchUserRatings = async () => {
            const token = localStorage.getItem('token');

            if (!token) {
                setMessage('You need to be logged in to view your ratings');
                setLoading(false);
                return;
            }

            try {
                const res = await axios.get(`${import.meta.env.VITE_API_URL}/movies/user/ratings`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
        });

    setUserRatings(res.data.ratings || []);
} catch (error) {
    console.error('Failed to fetch user ratings:', error);
    setMessage('Failed to fetch user ratings. Please try again.');
} finally {
    setLoading(false);
}
        };

fetchUserRatings();
    }, []);

return (
    <div>
        <h1>My Ratings</h1>

        {}
        {loading ? (
            <div className="loader-container">
                <ClipLoader size={50} color="#36d7b7" loading={loading} />
            </div>
        ) : (
            <>
                {message && <p>{message}</p>}
                {userRatings.length > 0 ? (
                    <ul>
                        {userRatings.map((rating) => (
                            <li key={rating.movie_id}>
                                <h3>{rating.movie_title} - Rating: {rating.rating}</h3>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>You have not rated any movies yet.</p>
                )}
            </>
        )}
    </div>
);
};

export default MyRatings;
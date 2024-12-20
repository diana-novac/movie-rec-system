import { useState } from 'react';
import axios from 'axios';

const RateMovieForm = ({ movieId, onSuccess }) => {
    const [rating, setRating] = useState('');
    const [message, setMessage] = useState('');

    const handleRate = async () => {
        const token = localStorage.getItem('token');

        if (!token) {
            setMessage('You must be logged in to rate a movie');
            return;
        }

        try {
            const res = await axios.post(
                `${import.meta.env.VITE_API_URL}/movies/rate`,
                { movie_id: movieId, rating },
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            setMessage(res.data.message);
            setRating('');
            onSuccess();
        } catch (error) {
            setMessage('Failed to rate movie');
        }
    };

    return (
        <div>
            <input
                type="number"
                min="1"
                max="5"
                placeholder="Rating (1-5)"
                value={rating}
                onChange={(e) => setRating(e.target.value)}
            />
            <button onClick={handleRate}>Rate</button>
            {message && <p>{message}</p>}
        </div>
    );
};

export default RateMovieForm;
import { useState } from 'react';
import axios from 'axios';

const RateMovie = () => {
  const [formData, setFormData] = useState({ movie_id: '', rating: '' });
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');

    if (!token) {
      setMessage('You must be logged in to rate a movie');
      return;
    }

    try {
      const res = await axios.post(
        `${import.meta.env.VITE_API_URL}/movies/rate`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setMessage(res.data.message);
    } catch (error) {
      console.error('Failed to rate movie:', error);
      setMessage('Failed to rate movie');
    }
  };

  return (
    <div>
      <h1>Rate a Movie</h1>
      <form onSubmit={handleSubmit}>
        <input
          name="movie_id"
          placeholder="Movie ID"
          value={formData.movie_id}
          onChange={handleChange}
          required
        />
        <input
          name="rating"
          type="number"
          min="1"
          max="5"
          placeholder="Rating (1-5)"
          value={formData.rating}
          onChange={handleChange}
          required
        />
        <button type="submit">Submit Rating</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default RateMovie;

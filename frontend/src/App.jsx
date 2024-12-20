import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Homepage from './pages/Homepage';
import Register from './pages/Register';
import Login from './pages/login';
import Navbar from './components/navbar';
import Movies from './pages/movies';
import Recommendations from './pages/recommendations';
import MyRatings from './pages/my_ratings';
import './App.css';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/movies" element={<Movies />} />
        <Route path="/recommendations" element={<Recommendations />} />
        <Route path = "/my-ratings" element={<MyRatings />} />
      </Routes>
    </Router>
  );
}

export default App;

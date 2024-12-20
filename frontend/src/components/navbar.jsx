import { Link } from 'react-router-dom';

const Navbar = () => {
    return (
        <nav>
            <h1>Movie Recommender</h1>
            <ul>
                <li>
                    <Link to="/">Home</Link>
                </li>
                <li>
                    <Link to="/movies">Movies</Link>
                </li>
                <li>
                    <Link to="/recommendations">Recommendations</Link>
                </li>
                <li>
                    <Link to="/login">Login</Link>
                </li>
                <li>
                    <Link to="/register">Register</Link>
                </li>
            </ul>
        </nav>
    );
};

export default Navbar;
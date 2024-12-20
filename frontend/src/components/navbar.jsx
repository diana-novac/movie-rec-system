import { Link, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';

const Navbar = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const navigate = useNavigate();  // Folosim useNavigate în loc de useHistory

    useEffect(() => {
        // Verificăm dacă există un token JWT stocat în localStorage
        const token = localStorage.getItem('token');
        if (token) {
            setIsLoggedIn(true); // Utilizatorul este logat
        }
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('token'); // Eliminăm token-ul
        setIsLoggedIn(false); // Actualizăm starea
        navigate('/'); // Redirecționăm utilizatorul la home
    };

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
                {isLoggedIn ? (
                    <>
                        <li>
                            <button onClick={handleLogout}>Logout</button>
                        </li>
                    </>
                ) : (
                    <>
                        <li>
                            <Link to="/login">Login</Link>
                        </li>
                        <li>
                            <Link to="/register">Register</Link>
                        </li>
                    </>
                )}
            </ul>
        </nav>
    );
};

export default Navbar;

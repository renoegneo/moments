import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Navbar.css';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          Наши моменты
        </Link>

        <div className="navbar-menu">
          {user ? (
            <>
              <Link to="/" className="navbar-link">Лента</Link>
              <Link to={`/profile/${user.id}`} className="navbar-link">Профиль</Link>
              <button onClick={handleLogout} className="navbar-button">
                Выйти
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="navbar-link">Вход</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
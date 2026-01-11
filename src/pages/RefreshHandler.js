import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function RefreshHandler({ setIsAuthenticated }) {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const loggedInUser = localStorage.getItem('loggedInUser');

    if (token && loggedInUser) {
      setIsAuthenticated(true);
      // If on login/signup, redirect to home
      if (window.location.pathname === '/' || window.location.pathname === '/login' || window.location.pathname === '/signup') {
        navigate('/home');
      }
    } else {
      setIsAuthenticated(false);
      // Redirect to login if trying to access protected routes
      if (window.location.pathname !== '/login' && window.location.pathname !== '/signup') {
        navigate('/login');
      }
    }
  }, [navigate, setIsAuthenticated]);

  return null; // This component doesn't render anything
}

export default RefreshHandler;

import { Navigate,Route, Routes } from 'react-router-dom';
import './App.css';
import Login from './pages/login';
import Signup from './pages/Signup';
import Home from './pages/Home';
import {useState, useEffect} from 'react';
import RefreshHandler from './pages/RefreshHandler';

function App() {

  const [isAuthenticated, setIsAuthenticated]= useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const loggedInUser = localStorage.getItem('loggedInUser');
    if (token && loggedInUser) {
      setIsAuthenticated(true);
    }
  }, []);

  const PrivateRoute = ({element})=>{
    return isAuthenticated ? element : <Navigate to="/login" /> 
  }
  return (
    <div className="App">
      <RefreshHandler setIsAuthenticated={setIsAuthenticated} />
      <header className="App-header">
          <Routes>
            <Route path='/' element={<Navigate to="/login" />} />
            <Route path='/login' element={<Login />} />
            <Route path='/signup' element={<Signup />}/>
            <Route path='/home' element={<PrivateRoute element={<Home setIsAuthenticated={setIsAuthenticated} />}/>}/>
          </Routes>
      </header>
    </div>
  );
}

export default App;

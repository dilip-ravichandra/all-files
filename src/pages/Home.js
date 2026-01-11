import React from 'react'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom' ;
import { handleSuccess} from '../utils';
import {ToastContainer} from 'react-toastify';
import { handleError } from '../utils';
function Home({ setIsAuthenticated }) {
  const [loggedInUser, setLoggedInUser] = useState('');
  const navigate = useNavigate();

  useEffect(() =>{
    setLoggedInUser(localStorage.getItem('loggedInUser'))
  },[])

  const handleLogout =(e) => {
    localStorage.removeItem('token');
    localStorage.removeItem('loggedInUser');
    setLoggedInUser('');
    setIsAuthenticated(false);
    setTimeout(() => {
      navigate('/login');
    }, 1000)
  }

  const fetchProducts = async () => {
    try {
      const url = "http://localhost:8080/products";
      const headers = {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
      const response = await fetch(url,headers);
      const result = await response.json(); 
      console.log(result);

    }
    catch (err) {
      handleError(err);
    }
  }
  useEffect(() => {
    fetchProducts();
  }, [])
  return (
    <div className='container'>
      <h1>Welcome to the Home Page</h1>
      <p>This is a simple home page content. You can add more features here.</p>
      {loggedInUser && <h2>Hello, {loggedInUser}!</h2>}
      <button onClick={handleLogout}>Logout</button>
      <ToastContainer />
    </div>
  )
}

export default Home
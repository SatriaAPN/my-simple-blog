import React, { useState, useEffect } from 'react';
import axios from 'axios'; 
import './RegisterPage.css'; 
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext'

const RegisterPage = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null); 
  const navigate = useNavigate(); 

  const context = useAuth();

  useEffect(() => {
    if (context.accessToken) {
      console.log('Access token found, navigating to home page...');
      navigate('/');
    }
  }, [context.accessToken, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault(); 

    if (!email || !password) {
      setError('Please fill in all fields');
      return;
    }

    try {
      const response = await axios.post(
        'http://localhost:8000/api/auth/register/', 
        {
          name,
          email,
          password,
        },
        {
          headers: { 'Content-Type': 'application/json' },
        }
      );

      alert('Register Successful!');

      navigate('/login');
    } catch (err) {
      console.error('Error:', err);
      if (err.response && err.response.data && err.response.data.errors) {
        setError(err.response.data.errors[0].detail);
      }
      else
        setError('Invalid email or password');
    }
  };

  return (
    <div className="register-container">
      <h2>Register</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name:</label>
          <input
            type="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default RegisterPage;

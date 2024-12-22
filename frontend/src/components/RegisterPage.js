import React, { useState } from 'react';
import axios from 'axios'; // Import Axios
import './RegisterPage.css'; // CSS for styling
import { useNavigate } from 'react-router-dom';

const RegisterPage = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null); // To handle errors
  const navigate = useNavigate(); // Hook for navigation

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent page reload

    // Basic Validation
    if (!email || !password) {
      setError('Please fill in all fields');
      return;
    }

    try {
      // Replace this URL with your backend API endpoint
      const response = await axios.post(
        'http://localhost:8000/api/auth/register', 
        {
          name,
          email,
          password,
        },
        {
          headers: { 'Content-Type': 'application/json' }, // No CSRF headers needed
        }
      );

      console.log('Response:', response.data);
      alert('Register Successful!'); // Replace with proper navigation or state updates
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
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default RegisterPage;

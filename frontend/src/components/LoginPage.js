import React, { useState } from 'react';
import axios from 'axios'; // Import Axios
import './LoginPage.css'; // CSS for styling

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null); // To handle errors

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
        'http://localhost:8000/api/auth/login', 
        {
          email,
          password,
        },
        {
          headers: { 'Content-Type': 'application/json' }, // No CSRF headers needed
        }
      );

      console.log('Response:', response.data);
      alert('Login Successful!'); // Replace with proper navigation or state updates
    } catch (err) {
      console.error('Error:', err);
      setError('Invalid email or password');
    }
  };

  return (
    
    <div className="login-container">
      <h2>Login</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
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

export default LoginPage;
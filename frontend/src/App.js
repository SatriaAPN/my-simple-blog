import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import LogoutPage from './components/LogoutPage';
import RegisterPage from './components/RegisterPage'
import HomePage from './components/HomePage'
import { AuthProvider } from './AuthContext'; // Import the provider
import Navbar from './components/Navbar';  // Import Navbar


function App() {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <div id="content" className='content-container'>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/logout" element={<LogoutPage />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;

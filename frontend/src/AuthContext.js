import React, { createContext, useContext, useState, useEffect } from 'react';
import { jwtDecode } from "jwt-decode";
import axios from 'axios';

// Create Context
const AuthContext = createContext();

// Provider Component
export const AuthProvider = ({ children }) => {
  // Get tokens from localStorage on load
  const [accessToken, setAccessToken] = useState(localStorage.getItem('accessToken') || null);
  const [refreshToken, setRefreshToken] = useState(localStorage.getItem('refreshToken') || null);

  // Save tokens in localStorage
  const saveTokens = (access, refresh) => {
    setAccessToken(access);
    setRefreshToken(refresh);
    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
  };

  const clearTokens = () => {
    setAccessToken(null);
    setRefreshToken(null);
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  };

  const checkTokenExp = () => {
    console.log('checking token exp')

    if (accessToken == null) {
      console.log('accessToken is empty')
      return false
    }

    if (isExpired(refreshToken)) {
      console.log("refresh token expired")
      clearTokens()

      return true
    }

    if (!isExpired(accessToken)) {
      console.log("access token not expired")
      return false
    }

    console.log("access token expired")


    try {
      axios.post(
        'http://localhost:8000/api/token/refresh/', 
        {
          refresh_token: refreshToken,
        },
        {
          headers: { 'Content-Type': 'application/json' },
        }
      ).then((response => {
        console.log("response1", response)
        console.log("response2", response.data)
        console.log(response.data.data.attributes)
        console.log("before", accessToken)
        setAccessToken(response.data.data.attributes.access_token);
        localStorage.setItem('accessToken', response.data.data.attributes.access_token);
        console.log("after", accessToken)
        return false
      }), (err) => {throw err})
    } catch (err) {
      console.log(err)
      console.log("refreshing access token failed, proceed to login page..")
      clearTokens()
      return true
    }
  }

  const isExpired = (token) => {
    try {
      const decoded = jwtDecode(token);
      const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds
      return decoded.exp < currentTime; // true if expired
    } catch (error) {
      console.error("Invalid token:", error);
      return true; // Treat invalid tokens as expired
    }
  }

  // Automatically clear tokens on logout or session expiry
  useEffect(() => {
    const handleStorageChange = () => {
      const storedAccessToken = localStorage.getItem('accessToken');
      if (!storedAccessToken) {
        clearTokens(); // Clear state if tokens are removed elsewhere
      }
    };
    window.addEventListener('storage', handleStorageChange);

    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  return (
    <AuthContext.Provider value={{ accessToken, refreshToken, saveTokens, clearTokens, checkTokenExp }}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook to use the context
export const useAuth = () => useContext(AuthContext);

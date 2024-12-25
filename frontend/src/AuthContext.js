import React, { createContext, useContext, useState, useEffect } from 'react';
import { jwtDecode } from "jwt-decode";
import axios from 'axios';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [accessToken, setAccessToken] = useState(localStorage.getItem('accessToken') || null);
  const [refreshToken, setRefreshToken] = useState(localStorage.getItem('refreshToken') || null);

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
    if (accessToken == null) {
      console.log('accessToken is empty')
      return false
    }

    console.log('checking accessToken expiration')

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
      console.log("refreshing access token")
      axios.post(
        'http://localhost:8000/api/token/refresh/', 
        {
          refresh_token: refreshToken,
        },
        {
          headers: { 'Content-Type': 'application/json' },
        }
      ).then((response => {
        setAccessToken(response.data.data.attributes.access_token);
        localStorage.setItem('accessToken', response.data.data.attributes.access_token);
        return false
      }), (err) => {throw err})
    } catch (err) {
      console.log("refreshing access token failed, proceed to login page..", err)
      clearTokens()
      return true
    }
  }

  const isExpired = (token) => {
    try {
      const decoded = jwtDecode(token);
      const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds
      return decoded.exp < currentTime;
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

export const useAuth = () => useContext(AuthContext);

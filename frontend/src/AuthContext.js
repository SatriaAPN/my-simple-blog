import React, { createContext, useContext, useState, useEffect } from 'react';

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
    <AuthContext.Provider value={{ accessToken, refreshToken, saveTokens, clearTokens }}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook to use the context
export const useAuth = () => useContext(AuthContext);

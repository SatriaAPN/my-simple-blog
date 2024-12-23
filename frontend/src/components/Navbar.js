import React from 'react';
// import { Link } from 'react-router-dom';
import { useAuth } from '../AuthContext'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';


const Navbar = () => {
  const context = useAuth();
  console.log('navbar AuthContext:', context);

  let loginOrLogout = "Logout"
  let loginOrLogoutUrl = "/logout"

  if (context.accessToken == null) {
    loginOrLogout = "Login"
    loginOrLogoutUrl = "/login"
  }

  return (
    <nav style={navbarStyle}>
      <ul style={ulStyle}>
        <li style={liStyle}>
          <Link to="/" style={linkStyle}>Home</Link>
        </li>
        <li style={liStyle}>
          <Link to={loginOrLogoutUrl} style={linkStyle}>{loginOrLogout}</Link>
        </li>
        {context.accessToken == null && ( // Render "Register" button conditionally
          <li style={liStyle}>
            <Link to="/register" style={linkStyle}>Register</Link>
          </li>
        )}
      </ul>
    </nav>
  );
};

const navbarStyle = {
  backgroundColor: '#333',
  padding: '10px 20px',
  display: 'flex',
  justifyContent: 'flex-end',
};

const ulStyle = {
  listStyleType: 'none',
  display: 'flex',
  justifyContent: 'center', // Centers the items horizontally
  alignItems: 'center',     // Aligns the items vertically if needed
  padding: 0,
  margin: 0,
};

const liStyle = {
  margin: '0 15px', // Space between menu items
};

const linkStyle = {
  color: 'white',
  textDecoration: 'none',
  fontSize: '16px',
};

export default Navbar;

import React, {useEffect} from 'react';
import { useAuth } from '../AuthContext'
import { Link, useNavigate } from 'react-router-dom';


const Navbar = () => {
  const context = useAuth();
  const navigate = useNavigate(); // Hook for navigation
  console.log('navbar AuthContext:', context);

  let loginOrLogout = "Logout"
  let loginOrLogoutUrl = "/logout"
  console.log('navbar AuthContext2:', context);

  if (context.accessToken == null) {
    loginOrLogout = "Login"
    loginOrLogoutUrl = "/login"
  }
  console.log('navbar AuthContext3:', context);

  useEffect(() => {
    console.log("navbar useeffect")
    if (context.checkTokenExp()) {
      console.log("whoaa expired")

      alert('session time is out, please login again'); // Replace with proper navigation or state updates

      // navigate('/login');
    }

  }, [context, navigate]);

  return (
    <nav style={navbarStyle}>
      <ul style={ulStyle}>
        <li style={liStyle}>
          <Link to="/" style={linkStyle}>Home</Link>
        </li>
        {context.accessToken != null && ( // Render "Register" button conditionally
          <li style={liStyle}>
            <Link to="/blogs/create" style={linkStyle}>Create Blog</Link>
          </li>
        )}
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
  backgroundColor: '#3d86d0',
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

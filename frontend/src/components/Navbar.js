import React, {useEffect} from 'react';
import { useAuth } from '../AuthContext'
import { Link, useNavigate } from 'react-router-dom';


const Navbar = () => {
  const context = useAuth();
  const navigate = useNavigate();
  console.log('navbar AuthContext:', context);

  let loginOrLogout = "Logout"
  let loginOrLogoutUrl = "/logout"

  if (context.accessToken == null) {
    loginOrLogout = "Login"
    loginOrLogoutUrl = "/login"
  }

  useEffect(() => {
    if (context.checkTokenExp()) {
      alert('session time is out, please login again');

      navigate('/login');
    }

  }, [context, navigate]);

  return (
    <nav style={navbarStyle}>
      <ul style={ulStyle}>
        <li style={liStyle}>
          <Link to="/" style={linkStyle}>Home</Link>
        </li>
        {context.accessToken != null && context.userRole === "writer" && ( 
          <li style={liStyle}>
            <Link to="/blogs/create" style={linkStyle}>Create Blog</Link>
          </li>
        )}
        {context.accessToken != null && context.userRole === "admin" && ( 
          <li style={liStyle}>
            <Link to="/admin/blogs" style={linkStyle}>Admin Blog Management</Link>
          </li>
        )}
        <li style={liStyle}>
          <Link to={loginOrLogoutUrl} style={linkStyle}>{loginOrLogout}</Link>
        </li>
        {context.accessToken == null && (
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
  justifyContent: 'center',
  alignItems: 'center', 
  padding: 0,
  margin: 0,
};

const liStyle = {
  margin: '0 15px', 
};

const linkStyle = {
  color: 'white',
  textDecoration: 'none',
  fontSize: '16px',
};

export default Navbar;

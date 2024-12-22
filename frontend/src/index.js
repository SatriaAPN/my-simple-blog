import React from 'react';
import ReactDOM from 'react-dom/client'; // Import from 'react-dom/client' in React 18+
import App from './App';
import Navbar from './Navbar';

// Create the root for the navbar
const navbarRoot = ReactDOM.createRoot(document.getElementById('root-0'));
navbarRoot.render(<Navbar />);

// Create the root for the page content
const contentRoot = ReactDOM.createRoot(document.getElementById('root-1'));
contentRoot.render(<App />);

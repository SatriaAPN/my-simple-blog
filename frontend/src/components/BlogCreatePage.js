import React, { useState, useEffect } from 'react';
import axios from 'axios'; // Import Axios
import './RegisterPage.css'; // CSS for styling
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext'

import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';
import Typography from '@mui/material/Typography';

const BlogCreatePage = () => {
  const [title, setTitle] = useState('');      // State for title
  const [content, setContent] = useState('');  // State for content
  const [error, setError] = useState(null); // To handle errors
  const navigate = useNavigate(); // Hook for navigation
  const context = useAuth();

  useEffect(() => {
    if (context.accessToken == null) {
      console.log('unauthorized');
      navigate('/login');
    }
  }, [context.accessToken, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent page reload

    // Basic Validation
    if (!title || !content) {
      setError('Please fill in all fields');
      return;
    }

    try {
      // Replace this URL with your backend API endpoint
      const response = await axios.post(
        'http://localhost:8000/api/blogs', 
        {
          title,
          content,
        },
        {
          headers: { 'Content-Type': 'application/json' }, // No CSRF headers needed
        }
      );

      console.log('Response:', response.data);
      alert('Create Blog Successful!'); // Replace with proper navigation or state updates
      // navigate('/');
      
    } catch (err) {
      console.error('Error:', err);
      if (err.response && err.response.data && err.response.data.errors) {
        setError(err.response.data.errors[0].detail);
      }
      else
        setError('something is wrong');
    }
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit} // Attach the submit handler
      sx={{ '& > :not(style)': { m: 1, width: '80ch' } }}
      noValidate
      autoComplete="off"
    >
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <Typography variant="h4" gutterBottom>
          Create Blog
        </Typography>
      </div>
      <div>
        <TextField
          id="outlined-title"
          label="Title"
          multiline
          variant="outlined"
          rows={2}
          fullWidth
          value={title}
          onChange={(e) => setTitle(e.target.value)} // Update title
        />
      </div>
      <div>
        <TextField
          id="outlined-content"
          label="Content"
          multiline
          variant="outlined"
          rows={25}
          fullWidth
          value={content}
          onChange={(e) => setContent(e.target.value)} // Update content
        />
      </div>
      {error && (
        <Typography color="error" variant="body2">
          {error}
        </Typography>
      )}
      <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          type="submit" // Submit button
          variant="contained"
          endIcon={<SendIcon />}
          sx={{ width: '150px' }}
        >
          Create
        </Button>
      </div>
    </Box>
  );
};

export default BlogCreatePage;

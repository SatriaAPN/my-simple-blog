import React, { useState, useEffect } from 'react';
import axios from 'axios'; 
import './RegisterPage.css'; 
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext'

import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';
import Typography from '@mui/material/Typography';

const BlogCreatePage = () => {
  const [title, setTitle] = useState(''); 
  const [content, setContent] = useState(''); 
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const context = useAuth();

  useEffect(() => {
    if (context.accessToken == null) {
      console.log('unauthorized, proceed to login page');
      navigate('/login');
    } 
  }, [context.accessToken, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent page reload

    if (!title || !content) {
      setError('Please fill in all fields');
      return;
    }

    // refreshing the access token before sending request
    if (!context.checkTokenExp()) {
      try {
        const response = await axios.post(
          'http://localhost:8000/api/blogs/', 
          {
            title,
            content,
          },
          {
            headers: { 
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${context.accessToken}`
            },
          }
        );

        alert('Create Blog Successful!');

        navigate('/');
      } catch (err) {
        console.error('Error:', err);
        if (err.response && err.response.data && err.response.data.errors) {
          setError(err.response.data.errors[0].detail);
        }
        else
          setError('something is wrong, please try again');
      }
    } else{
      alert('session time is out, please login again');

      navigate('/login');
    }
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
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
          onChange={(e) => setTitle(e.target.value)}
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
          onChange={(e) => setContent(e.target.value)}
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

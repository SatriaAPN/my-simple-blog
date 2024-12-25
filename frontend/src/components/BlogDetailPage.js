import React, { useState, useEffect } from 'react';
import axios from 'axios'; 
import './RegisterPage.css';
import { useParams } from 'react-router-dom';

import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

const BlogDetailPage = () => {
  const { title } = useParams(); 
  const [blogData, setBlogData] = useState(null);
  const [loading, setLoading] = useState(true); 
  const [error, setError] = useState(null); 

  useEffect(() => {
    const fetchBlogData = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/api/blogs/${title}/`, 
          {
            headers: { 'Content-Type': 'application/json' },
          }
        );

        if (response.statusText !== "OK") {
          throw new Error('Blog not found');
        } 

        const data = response.data.data;

        setBlogData(data); 
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    // Call the fetch function
    fetchBlogData();
  }, [title]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <Box
      sx={{ '& > :not(style)': { m: 1, width: '80ch' } }}
      noValidate
      autoComplete="off"
    >
      <div>
        <Typography variant="h4" gutterBottom>
          {blogData?.attributes?.title}
        </Typography>
      </div>
      <div>
        <Typography variant="body2" gutterBottom>
          {blogData?.attributes?.content}
        </Typography>
      </div>
    </Box>
  );
};

export default BlogDetailPage;

import React, { useState, useEffect } from 'react';
import axios from 'axios'; // Import Axios
import './RegisterPage.css'; // CSS for styling
import { useParams } from 'react-router-dom';

import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

const BlogDetailPage = () => {
  const { title } = useParams(); // Extract the 'title' parameter from the URL
  const [blogData, setBlogData] = useState(null);
  const [loading, setLoading] = useState(true); // Loading state
  const [error, setError] = useState(null); // Error state

  useEffect(() => {
    const fetchBlogData = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/api/blogs/${title}/`, 
          {
            headers: { 'Content-Type': 'application/json' }, // No CSRF headers needed
          }
        );
        console.log(response)

        if (response.statusText !== "OK") {
          throw new Error('Blog not found');
        } 
        const data = response.data.data;
        setBlogData(data); // Set the fetched data
      } catch (error) {
        setError(error.message); // Handle errors
      } finally {
        setLoading(false); // Set loading to false once done
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

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider'; // For section separation

const HomePage = () => {
  const [blogs, setBlogs] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const navigate = useNavigate();

  // Fetch blogs from the API
  const fetchBlogs = async (page) => {
    try {
      const response = await axios.get(
        `http://localhost:8000/api/blogs?page=${page}`
      );

      // Update blogs and pagination info
      setBlogs(response.data.data || []);
      setTotalPages(
        Math.ceil(response.data.meta.total / response.data.meta.blogPerPage)
      );
    } catch (error) {
      console.error('Error fetching blogs:', error);
    }
  };

  // Handle page change
  const handlePageChange = (event, value) => {
    setPage(value);
  };

  // Navigate to blog URL
  const handleNavigate = (url) => {
    navigate(`/blogs/${url}`);
  };

  // Fetch blogs whenever page changes
  useEffect(() => {
    fetchBlogs(page);
  }, [page]);

  return (
    <Stack spacing={4} marginTop={5} alignItems={'center'}>
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        Latest Blogs
      </Typography>
      <Divider sx={{ width: '80%' }} />

      {blogs.map((blog, index) => (
        <Box
          key={index}
          sx={{
            width: 600,
            padding: 2,
            borderRadius: 2,
            boxShadow: 3,
            bgcolor: '#ffffff',
            transition: 'all 0.3s ease',
            '&:hover': {
              boxShadow: 6,
              transform: 'scale(1.02)',
              cursor: 'pointer',
            },
          }}
          onClick={() => handleNavigate(blog.url)}
        >
          <Typography variant="h5" fontWeight="bold" gutterBottom>
            {blog.title}
          </Typography>
          <Typography variant="body2" color="textSecondary">
            Published on: {new Date(blog.createdAt).toLocaleDateString()}
          </Typography>
        </Box>
      ))}

      <Pagination
        count={totalPages}
        color="primary"
        page={page}
        onChange={handlePageChange}
        sx={{ marginTop: 2 }}
      />
    </Stack>
  );
};

export default HomePage;

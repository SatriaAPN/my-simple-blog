import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import Button from '@mui/material/Button';
import Pagination from '@mui/material/Pagination';

const HomePage = () => {
  const [blogs, setBlogs] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const navigate = useNavigate();
  const context = useAuth();

  const fetchBlogs = async (page) => {
    try {
      const response = await axios.get(
        `http://localhost:8000/api/blogs?page=${page}&pageView=admin-management`,
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${context.accessToken}`,
          },
        }
      );

      setBlogs(response.data.data || []);
      setTotalPages(
        Math.ceil(response.data.meta.total / response.data.meta.blogPerPage)
      );
    } catch (error) {
      console.error('Error fetching blogs:', error);
    }
  };

  const handleNavigate = (url) => {
    navigate(`/blogs/${url}`);
  };

  const handleHide = async (url) => {
    try {
      const response = await axios.post(
        'http://localhost:8000/api/admin/blogs/hide/',
        {
          url: url,
          hide: true,
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${context.accessToken}`,
          },
        }
      );

      fetchBlogs(page);
    } catch (error) {
      console.error('Error hiding blog:', error);
      alert('Failed to hide blog.');
    }
  };

  const handleUnhide = async (url) => {
    try {
      const response = await axios.post(
        'http://localhost:8000/api/admin/blogs/hide/',
        {
          url: url,
          hide: false,
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${context.accessToken}`,
          },
        }
      );

      fetchBlogs(page);
    } catch (error) {
      console.error('Error hiding blog:', error);
      alert('Failed to hide blog.');
    }
  };

  const handlePageChange = (event, value) => {
    setPage(value);
  };

  useEffect(() => {
    if (context.accessToken == null || context.userRole !== 'admin') {
      console.log('unauthorized, proceed to login page');
      navigate('/');
    }

    fetchBlogs(page);
  }, [context, page]);

  return (
    <Stack spacing={4} marginTop={5} alignItems={'center'}>
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        Latest Blogs
      </Typography>
      <Divider sx={{ width: '80%' }} />

      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} size="small" aria-label="blog table">
          <TableHead>
            <TableRow>
              <TableCell>Title</TableCell>
              <TableCell align="center">Created At</TableCell>
              <TableCell align="center">Actions</TableCell>
              <TableCell align="center">Hiden / Unhiden</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {blogs.map((blog) => (
              <TableRow key={blog.url}>
                <TableCell component="th" scope="row">
                  {blog.title}
                </TableCell>
                <TableCell align="center">
                  {new Date(blog.createdAt).toLocaleString()}
                </TableCell>
                <TableCell align="center">
                  <Button
                    variant="outlined"
                    size="small"
                    onClick={() => handleNavigate(blog.url)}
                  >
                    View
                  </Button>
                </TableCell>
                <TableCell align="center">
                  {!blog.isHiden && (
                    <Button
                      variant="outlined"
                      size="small"
                      color="error"
                      sx={{ marginLeft: 1 }}
                      onClick={() => handleHide(blog.url)}
                    >
                      Hide
                    </Button>
                  )}
                  {blog.isHiden && (
                    <Button
                      variant="outlined"
                      size="small"
                      sx={{ marginLeft: 1 }}
                      onClick={() => handleUnhide(blog.url)}
                    >
                      Unhide
                    </Button>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

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

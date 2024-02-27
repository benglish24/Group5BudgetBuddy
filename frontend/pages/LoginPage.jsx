// Create a new file, e.g., MUIShapedLogin.js

import { Button, Card, CardContent, TextField, Typography } from '@mui/material';
import React, { useState, useContext } from 'react';
import Link from 'next/link'

import Dashboard from './Dashboard';

import AuthContext from './context/AuthContext';

const cardStyle = {
  maxWidth: '400px',
  margin: 'auto',
  marginTop: '100px',
  padding: '20px',
  textAlign: 'center',
};

const inputStyle = {
  marginBottom: '20px',
  width: '100%',
};

const LoginPage = () => {

  const {loginUser} = useContext(AuthContext)

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleLogin = (e) => {
    e.preventDefault() // REQUIRED FOR REQUESTS TO GO THROUGH (don't know why)

    // Implement your login logic here
    console.log('Logging in with:', { username, password });
    // Example: You can send a request to a server to verify credentials
    username.length > 0 && loginUser(username, password)

  };

  return (
    <Card sx={cardStyle}>
      <CardContent>
        <Typography variant="h4" gutterBottom>
          Login
        </Typography>

        <form onSubmit={handleLogin}>
          <TextField
            label="Username"
            variant="outlined"
            sx={inputStyle}
            value={username}
            onChange={handleUsernameChange}
          />
          <TextField
            label="Password"
            variant="outlined"
            type="password"
            sx={inputStyle}
            value={password}
            onChange={handlePasswordChange}
          />
          <Button type="submit" variant="contained" color="primary">
            Login
          </Button>
        </form>

        <Link href="/Registration">Not signed up? Register here.</Link>
        
      </CardContent>
    </Card>
  );
};

export default LoginPage;

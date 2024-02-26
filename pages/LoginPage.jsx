// Create a new file, e.g., MUIShapedLogin.js

import { Button, Card, CardContent, TextField, Typography } from '@mui/material';
import React, { useState } from 'react';

import Dashboard from './Dashboard';

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
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleLogin = () => {
    // Implement your login logic here
    console.log('Logging in with:', { username, password });
    // Example: You can send a request to a server to verify credentials
  };

  return (
    <Card sx={cardStyle}>
      <CardContent>
        <Typography variant="h4" gutterBottom>
          Login
        </Typography>
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
        <Button variant="contained" color="primary" href="/dashboard">
          Login
        </Button>
      </CardContent>
    </Card>
  );
};

export default LoginPage;

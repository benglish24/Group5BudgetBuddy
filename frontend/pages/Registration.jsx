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

const Registration = () => {

  const {registerUser} = useContext(AuthContext)

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirm_password, setConfirmPassword] = useState('');

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleConfirmPasswordChange = (event) => {
    setConfirmPassword(event.target.value);
  };

  const handleRegistration = (e) => {
    e.preventDefault() // REQUIRED FOR REQUESTS TO GO THROUGH (don't know why)

    // Implement your login logic here
    console.log('Registering with:', { username, password, confirm_password});
    // Example: You can send a request to a server to verify credentials
    username.length > 0 && registerUser(username, password, confirm_password)

  };

  return (
    <Card sx={cardStyle}>
      <CardContent>
        <Typography variant="h4" gutterBottom>
          Registration
        </Typography>

        <form onSubmit={handleRegistration}>
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
          <TextField
            label="Confirm password"
            variant="outlined"
            type="password"
            sx={inputStyle}
            value={confirm_password}
            onChange={handleConfirmPasswordChange}
          />
          <Button type="submit" variant="contained" color="primary">
            Register
          </Button>
        </form>

        <Link href="/LoginPage" className='test'>Have an account? Sign in here.</Link>

      </CardContent>
    </Card>
  );
};

export default Registration;

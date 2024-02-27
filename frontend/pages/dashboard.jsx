import { AppBar, Container, CssBaseline, Drawer, List, ListItem, ListItemIcon, ListItemText, Toolbar, Typography } from '@mui/material';

import React, {useContext} from 'react';
import { useRouter } from 'next/router';


import AuthContext from './context/AuthContext';

const drawerWidth = 240;

const Dashboard = ({ children, navigateToDashboard, navigateToAnalytics }) => {

  const router = useRouter()
  const {user, logoutUser, authTokens} = useContext(AuthContext)

  // TODO: find better way of doing this. (maybe through a private route or w/e NextJS equivalent is)
  // if user not logged in, redirect to login. 
  if (!user) router.push("/LoginPage") 

  console.log(user, authTokens)

  const rootStyle = {
    display: 'flex',
  };

  const appBarStyle = {
    zIndex: 1201,
  };

  const drawerStyle = {
    width: drawerWidth,
    flexShrink: 0,
  };

  const drawerPaperStyle = {
    width: drawerWidth,
  };

  const drawerContainerStyle = {
    overflow: 'auto',
  };

  const contentStyle = {
    flexGrow: 1,
    padding: '20px',
  };

  // const navigateToLoginPage = () => {
  //   router.push('/LoginPage'); // Replace 'loginpage' with the actual path of your login page
  // };

  return (
    <div style={rootStyle}>
      <CssBaseline />
      <AppBar position="fixed" style={appBarStyle}>
        <Toolbar>
          <Typography variant="h6" noWrap>
            Dashboard
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer
        style={drawerStyle}
        variant="permanent"
        classes={{
          paper: drawerPaperStyle,
        }}
      >
        <Toolbar />
        <div style={drawerContainerStyle}>
          <List>
            <ListItem button onClick={navigateToDashboard}>
              
              <ListItemText primary="Dashboard" />
            </ListItem>
            <ListItem button onClick={navigateToAnalytics}>
              <ListItemText primary="Analytics" />
            </ListItem>
            <ListItem button onClick={logoutUser}>
              <ListItemText primary="Logout" />
            </ListItem>
            {/* Add more menu items as needed */}
          </List>
        </div>
      </Drawer>
      <main style={contentStyle}>
        <Toolbar />
        <Container maxWidth="lg">
        <h1>Hi, {user?.username}</h1>
          {children}
        </Container>
      </main>
    </div>
  );
};

export default Dashboard;

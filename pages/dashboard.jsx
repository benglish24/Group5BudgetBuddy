import { AppBar, Container, CssBaseline, Drawer, List, ListItem, ListItemIcon, ListItemText, Toolbar, Typography } from '@mui/material';

import React from 'react';
import { useRouter } from 'next/router';

const drawerWidth = 240;

const Dashboard = ({ children, navigateToDashboard, navigateToAnalytics }) => {
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

  const navigateToLoginPage = () => {
    router.push('/LoginPage'); // Replace 'loginpage' with the actual path of your login page
  };

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
            <ListItem button onClick={navigateToLoginPage}>
              <ListItemText primary="Back to Login" />
            </ListItem>
            {/* Add more menu items as needed */}
          </List>
        </div>
      </Drawer>
      <main style={contentStyle}>
        <Toolbar />
        <Container maxWidth="lg">
          {children}
        </Container>
      </main>
    </div>
  );
};

export default Dashboard;

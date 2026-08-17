import { Container, Typography, Box } from '@mui/material';
import AppHeader from './components/layouts/AppHeader.jsx';
import LoginForm from './components/auth/LoginForm.jsx';
import RobotDataGrid from './components/robots/RobotDataGrid.jsx';
import DiscrepancyDataGrid from './components/missions/DiscrepancyDataGrid.jsx';
import { AuthProvider, useAuth } from './context/AuthContext.jsx';

//main dashboard component that renders the application header and robot data grid
//to authenticated users
function Dashboard() {
  //stores the current user object and logout function from the global AuthContext
  const {user, logout} = useAuth();

  return (
      <>
        <AppHeader username={user?.sub} role={user?.role} onLogout={logout} />
        <Container maxWidth="lg" sx={{ mt: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom>
            Fleet Overview
          </Typography>
          <Box sx={{ mb: 4 }}>
            <RobotDataGrid />
          </Box>
          <Typography variant="h5" component="h2" gutterBottom>
          Co-Location Discrepancies
        </Typography>
        <Box sx={{ mb: 4 }}>
          <DiscrepancyDataGrid />
        </Box>
        </Container>
      </>
    );
  }

  //conditional layout switcher component that renders either the dashboard or the login form
  //based on the user's authentication status, tracked in the global AuthContext
function AppContent() {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <Dashboard /> : <LoginForm />;
}

//root application component that wraps the entire app in the AuthProvider context
function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
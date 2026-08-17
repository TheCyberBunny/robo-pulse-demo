import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {ThemeProvider, CssBaseline } from '@mui/material';
import theme from './theme.js';
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    {/* ThemeProvider is a component from Material-UI that allows you to apply 
    a custom theme to your application. In this case, we are wrapping the App
    component with the ThemeProvider and passing in the custom theme we created
    in theme.js. This will ensure that all Material-UI components within the 
    App component will use the custom theme settings. */}
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </StrictMode>,
)




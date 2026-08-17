import { createTheme } from '@mui/material/styles';

//the createTheme function is used to create a custom theme
//  for the Material-UI components. In this case, we are 
// defining a light mode theme with specific primary and 
// secondary colors, as well as a custom border radius for the components.
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#0d47a1',
    },
    secondary: {
      main: '#ff6f00',
    },
  },
  shape: {
    borderRadius: 8,
  },
});

export default theme;
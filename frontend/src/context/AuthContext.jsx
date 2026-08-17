import { createContext, useContext, useMemo, useState } from 'react';
import apiClient from '../api/client.js';

//creates a global React context which acts as a central store to hold authentication
//state so any component can access it without passing props down manually
const AuthContext = createContext(null);

//extracts and decodes the user payload from our JWT so that React can read it
//without calling the backend again
function decodeToken(token) {
  const payloadSegment = token.split('.')[1];
  return JSON.parse(atob(payloadSegment));
}

//AuthProvider is a component that wraps the application and manages authentication state
export function AuthProvider({ children }) {
    //initializes our token state from browser local storage to ensure a user stays logged
    //in even if they refresh the page, reading from storage only once on initial render
  const [token, setToken] = useState(() => localStorage.getItem('roboPulseToken'));

  //decodes the JWT into a user object and caches the results and prevents re-decoding
  //the token string on every re-render. It only runs when the token actually changes
  const user = useMemo(() => (token ? decodeToken(token) : null), [token]);

  //authenticates user credentials against the backend API by sending credentials,
  //saving the returned token to localStorage, and updates React state
  const login = async (username, password) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await apiClient.post('/auth/token', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });

    localStorage.setItem('roboPulseToken', response.data.access_token);
    setToken(response.data.access_token);
  };

  //clears the stored authentication session and resets state to null
  const logout = () => {
    localStorage.removeItem('roboPulseToken');
    setToken(null);
  };

  //bundles all auth state variables and action functions into a single object
  //to define the exact interface exposed to components consuming this context
  const value = { token, user, isAuthenticated: Boolean(token), login, logout };

  //renders the context provider and passes down the value object to make
  //the auth state and functions available to all nested child components
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

//a custom React hook that exposes the AuthContext to any component
//this simplifies context usage in child components 
// (useAuth() instead of useContext(AuthContext)) and throws an error if used outside of <AuthProvider>
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === null) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
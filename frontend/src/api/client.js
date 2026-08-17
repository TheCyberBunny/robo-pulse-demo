/**
 * RoboPulse Fleet Command Center
 * Day 7 - a single, shared Axios instance every component uses to
 * talk to the FastAPI backend, instead of each component configuring
 * its own request settings from scratch.
 */
import axios from 'axios';

//axios.create builds a reusable pre-configured client
const apiClient = axios.create({
    // this is our FastAPI endpoint
  baseURL: 'http://127.0.0.1:8000',
});

//the request interceptor runs on every outgoing request and checks if a token
//is sitting in localStorage. If so, it attaches it as the Authorization
//header automatically. Components do not need to remember to attach tokens
//making this the centralized place for token logic.
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('roboPulseToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
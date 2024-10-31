import axios from 'axios';

const API_URL = 'http://localhost:8000'; // Update this to your backend URL if different

export const api = axios.create({
  baseURL: API_URL,
  timeout: 5000, // Set timeout for API requests
});

// Function to set the Authorization token
export const setAuthToken = (token) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
};

// Add a response interceptor to handle errors globally
api.interceptors.response.use(
  response => response,
  error => {
    // You can add custom error handling here
    return Promise.reject(error);
  }
);

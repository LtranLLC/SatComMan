import React, { useState } from 'react';
import { api, setAuthToken } from '../services/api';
import { useNavigate, Link } from 'react-router-dom';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const [error, setError] = useState('');

  const handleLogin = async () => {
    try {
      const response = await api.post('/auth/token', {
        username: email,
        password: password,
      });
      const token = response.data.access_token;
      setAuthToken(token);
      navigate('/dashboard');
    } catch (err) {
      console.error('Login failed:', err);
      setError(err.response?.data?.detail || 'Login failed. Please try again.');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Login</h2>
      {error && <p style={{color: 'red'}}>{error}</p>}
      <input
        type="email"
        placeholder="Email"
        onChange={(e) => setEmail(e.target.value)}
        style={{ marginBottom: '10px', padding: '8px', width: '300px' }}
      /><br />
      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
        style={{ marginBottom: '10px', padding: '8px', width: '300px' }}
      /><br />
      <button onClick={handleLogin} style={{ padding: '10px 20px' }}>Login</button>
      <p>Don't have an account? <Link to="/register">Register here</Link>.</p> {/* Optional */}
    </div>
  );
}

export default Login;

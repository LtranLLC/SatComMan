import React, { useState } from 'react';
import { api } from '../services/api';
import { useNavigate, Link } from 'react-router-dom';

function Register() {
  const [form, setForm] = useState({
    name: '',
    email: '',
    phone_number: '',
    password: '',
    account_type: 'Prepaid', // Default account type
    imei: '',
  });
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({...form, [e.target.name]: e.target.value});
  };

  const handleRegister = async () => {
    try {
      await api.post('/users/', form);
      setMessage('Registration successful! Please log in.');
      navigate('/');
    } catch (err) {
      console.error('Registration failed:', err);
      setMessage(err.response?.data?.detail || 'Registration failed. Please try again.');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Register</h2>
      {message && <p>{message}</p>}
      <input
        type="text"
        name="name"
        placeholder="Name"
        onChange={handleChange}
        style={{ marginBottom: '10px', padding: '8px', width: '300px' }}
      /><br />
      <input
        type="email"
        name="email"
        placeholder="Email"
        onChange={handleChange}
        style={{ marginBottom: '10px', padding: '8px', width: '300px' }}
      /><br />
      <input
        type="text"
        name="phone_number"
        placeholder="Phone Number"
        onChange={handleChange}
        style={{ marginBottom: '10px', padding: '8px', width: '300px' }}
      /><br />
      <input
        type="text"
        name="imei"
        placeholder="IMEI"
        onChange={handleChange}
        style={{ marginBottom: '10px', padding: '8px', width: '300px' }}
      /><br />
      <input
        type="password"
        name="password"
        placeholder="Password"
        onChange={handleChange}
        style={{ marginBottom: '10px', padding: '8px', width: '300px' }}
      /><br />
      <select
        name="account_type"
        onChange={handleChange}
        style={{ marginBottom: '10px', padding: '8px', width: '310px' }}
      >
        <option value="Prepaid">Prepaid</option>
        <option value="Postpaid">Postpaid</option>
      </select><br />
      <button onClick={handleRegister} style={{ padding: '10px 20px' }}>Register</button>
      <p>Already have an account? <Link to="/">Login here</Link>.</p>
    </div>
  );
}

export default Register;

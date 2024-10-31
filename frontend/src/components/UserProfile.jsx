import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

function UserProfile() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/users/me')
      .then(response => {
        setUser(response.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching user:', err);
        setError('Failed to load user profile.');
        setLoading(false);
      });
  }, []);

  if (loading) return <div style={{ padding: '20px' }}>Loading...</div>;
  if (error) return <div style={{ padding: '20px', color: 'red' }}>{error}</div>;

  return (
    <div style={{ padding: '20px' }}>
      <h2>Profile</h2>
      <p><strong>Name:</strong> {user.name}</p>
      <p><strong>Email:</strong> {user.email}</p>
      <p><strong>Phone:</strong> {user.phone_number}</p>
      <p><strong>IMEI:</strong> {user.imei}</p>
      <p><strong>Account Type:</strong> {user.account_type}</p>
      <p><strong>Account Status:</strong> {user.account_status}</p>
      <p><strong>Balance:</strong> ${user.balance.toFixed(2)}</p>
    </div>
  );
}

export default UserProfile;

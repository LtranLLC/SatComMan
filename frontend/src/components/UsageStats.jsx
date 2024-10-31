import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

function UsageStats() {
  const [usage, setUsage] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/usage/me')
      .then(response => {
        setUsage(response.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching usage:', err);
        setError('Failed to load usage statistics.');
        setLoading(false);
      });
  }, []);

  if (loading) return <div style={{ padding: '20px' }}>Loading...</div>;
  if (error) return <div style={{ padding: '20px', color: 'red' }}>{error}</div>;
  if (usage.length === 0) return <div style={{ padding: '20px' }}>No usage data available.</div>;

  return (
    <div style={{ padding: '20px' }}>
      <h2>Usage Statistics</h2>
      <table border="1" cellPadding="10" cellSpacing="0">
        <thead>
          <tr>
            <th>Date</th>
            <th>Call Duration (min)</th>
            <th>Data Used (MB)</th>
          </tr>
        </thead>
        <tbody>
          {usage.map(record => (
            <tr key={record.usage_id}>
              <td>{new Date(record.timestamp).toLocaleDateString()}</td>
              <td>{record.call_duration}</td>
              <td>{record.data_used}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default UsageStats;

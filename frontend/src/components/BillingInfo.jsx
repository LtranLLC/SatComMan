import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

function BillingInfo() {
  const [billing, setBilling] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/billing/me')
      .then(response => {
        setBilling(response.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching billing:', err);
        setError('Failed to load billing information.');
        setLoading(false);
      });
  }, []);

  if (loading) return <div style={{ padding: '20px' }}>Loading...</div>;
  if (error) return <div style={{ padding: '20px', color: 'red' }}>{error}</div>;
  if (billing.length === 0) return <div style={{ padding: '20px' }}>No billing information available.</div>;

  return (
    <div style={{ padding: '20px' }}>
      <h2>Billing Information</h2>
      <table border="1" cellPadding="10" cellSpacing="0">
        <thead>
          <tr>
            <th>Billing Period Start</th>
            <th>Billing Period End</th>
            <th>Total Amount ($)</th>
            <th>Amount Due ($)</th>
            <th>Due Date</th>
            <th>Payment Status</th>
          </tr>
        </thead>
        <tbody>
          {billing.map(record => (
            <tr key={record.bill_id}>
              <td>{new Date(record.billing_period_start).toLocaleDateString()}</td>
              <td>{new Date(record.billing_period_end).toLocaleDateString()}</td>
              <td>{record.total_amount.toFixed(2)}</td>
              <td>{record.amount_due.toFixed(2)}</td>
              <td>{new Date(record.due_date).toLocaleDateString()}</td>
              <td>{record.payment_status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default BillingInfo;

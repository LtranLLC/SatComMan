import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

function Payments() {
  const [payments, setPayments] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/payments/me')
      .then(response => {
        setPayments(response.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching payments:', err);
        setError('Failed to load payments.');
        setLoading(false);
      });
  }, []);

  if (loading) return <div style={{ padding: '20px' }}>Loading...</div>;
  if (error) return <div style={{ padding: '20px', color: 'red' }}>{error}</div>;
  if (payments.length === 0) return <div style={{ padding: '20px' }}>No payments found.</div>;

  return (
    <div style={{ padding: '20px' }}>
      <h2>Payments</h2>
      <table border="1" cellPadding="10" cellSpacing="0">
        <thead>
          <tr>
            <th>Payment Date</th>
            <th>Amount ($)</th>
            <th>Payment Method</th>
          </tr>
        </thead>
        <tbody>
          {payments.map(payment => (
            <tr key={payment.payment_id}>
              <td>{new Date(payment.payment_date).toLocaleDateString()}</td>
              <td>{payment.amount.toFixed(2)}</td>
              <td>{payment.payment_method}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Payments;

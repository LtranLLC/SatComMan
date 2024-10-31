import React, { useState } from 'react';
import { api } from '../services/api';

function Recharge() {
  const [amount, setAmount] = useState('');
  const [message, setMessage] = useState('');

  const handleRecharge = async () => {
    try {
      await api.post('/users/recharge', { amount: parseFloat(amount) });
      setMessage('Recharge successful!');
    } catch (err) {
      console.error('Recharge failed:', err);
      setMessage(err.response?.data?.detail || 'Recharge failed. Please try again.');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Recharge Account</h2>
      {message && <p>{message}</p>}
      <input
        type="number"
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        style={{ marginBottom: '10px', padding: '8px', width: '200px' }}
      /><br />
      <button onClick={handleRecharge} style={{ padding: '10px 20px' }}>Recharge</button>
    </div>
  );
}

export default Recharge;

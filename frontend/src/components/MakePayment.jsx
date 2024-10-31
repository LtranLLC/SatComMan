import React, { useState } from 'react';
import { api } from '../services/api';

function MakePayment() {
  const [amount, setAmount] = useState('');
  const [paymentMethod, setPaymentMethod] = useState('');
  const [message, setMessage] = useState('');

  const handlePayment = async () => {
    try {
      const response = await api.post('/billing/pay/me', {
        amount: parseFloat(amount),
        payment_method: paymentMethod,
      });
      setMessage('Payment successful!');
    } catch (err) {
      console.error('Payment failed:', err);
      setMessage(err.response?.data?.detail || 'Payment failed. Please try again.');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Make a Payment</h2>
      {message && <p>{message}</p>}
      <input
        type="number"
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        style={{ marginBottom: '10px', padding: '8px', width: '200px' }}
      /><br />
      <select
        value={paymentMethod}
        onChange={(e) => setPaymentMethod(e.target.value)}
        style={{ marginBottom: '10px', padding: '8px', width: '210px' }}
      >
        <option value="">Select Payment Method</option>
        <option value="Credit Card">Credit Card</option>
        <option value="Debit Card">Debit Card</option>
        <option value="PayPal">PayPal</option>
        {/* Add more payment methods as needed */}
      </select><br />
      <button onClick={handlePayment} style={{ padding: '10px 20px' }}>Pay</button>
    </div>
  );
}

export default MakePayment;

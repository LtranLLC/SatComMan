import React from 'react';
import { Link } from 'react-router-dom';

function Dashboard() {
  return (
    <div style={{ padding: '20px' }}>
      <h2>User Dashboard</h2>
      <ul>
        <li><Link to="/profile">User Profile</Link></li>
        <li><Link to="/usage">Usage Statistics</Link></li>
        <li><Link to="/billing">Billing Information</Link></li> {/* Optional */}
        <li><Link to="/payments">Payment History</Link></li>        {/* Optional */}
        <li><Link to="/make-payment">Make a Payment</Link></li>     {/* Optional */}
        <li><Link to="/recharge">Recharge Account</Link></li>       {/* Optional */}
      </ul>
    </div>
  );
}

export default Dashboard;

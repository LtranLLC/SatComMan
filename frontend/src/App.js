import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';       // Optional
import Dashboard from './components/Dashboard';
import UserProfile from './components/UserProfile';
import UsageStats from './components/UsageStats';
import BillingInfo from './components/BillingInfo';  // Optional
import Payments from './components/Payments';        // Optional
import MakePayment from './components/MakePayment';  // Optional
import Recharge from './components/Recharge';        // Optional

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} /> {/* Optional */}
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<UserProfile />} />
        <Route path="/usage" element={<UsageStats />} />
        <Route path="/billing" element={<BillingInfo />} /> {/* Optional */}
        <Route path="/payments" element={<Payments />} />     {/* Optional */}
        <Route path="/make-payment" element={<MakePayment />} /> {/* Optional */}
        <Route path="/recharge" element={<Recharge />} />       {/* Optional */}
        {/* Add more routes as needed */}
      </Routes>
    </Router>
  );
}

export default App;

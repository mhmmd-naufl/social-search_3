import React, { useState } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Login from "./Login";
import Dashboard from "./Dashboard";
import PustakaMakna from "./pustaka-makna"; // Import halaman Pustaka Makna

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route
          path="/dashboard"
          element={isLoggedIn ? <Dashboard /> : <Navigate to="/login" />}
        />
        <Route
          path="/pustaka-makna"
          element={isLoggedIn ? <PustakaMakna /> : <Navigate to="/login" />} // Proteksi rute
        />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
import React, { useState } from "react";
import { FiEye, FiEyeOff } from "react-icons/fi";
import { useNavigate } from "react-router-dom";
import "./Login.css";
import bgImage from "./assets/bg.png";

const Login = ({ onLogin }) => {
  const [showPassword, setShowPassword] = useState(false);
  const [adminId, setAdminId] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const togglePasswordVisibility = () => {
    setShowPassword((prev) => !prev);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (adminId === "admin" && password === "1") {
      onLogin(); // panggil dari App.js
      navigate("/dashboard"); // pindah ke dashboard
    } else {
      alert("ID atau password salah");
    }
  };

  return (
    <div
      className="login-container"
      style={{
        backgroundImage: `linear-gradient(to bottom right, rgba(0, 0, 0, 0.7), rgba(0, 0, 255, 0.4), rgba(255, 255, 255, 0.1)), url(${bgImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div className="login-box">
        <h2>Login Admin</h2>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="adminId">Id Admin</label>
            <input
              type="text"
              id="adminId"
              placeholder="Masukkan Id Admin"
              value={adminId}
              onChange={(e) => setAdminId(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <div className="password-label">
              <label htmlFor="password">Password</label>
              <span
                className="toggle-password"
                onClick={togglePasswordVisibility}
              >
                {showPassword ? <FiEyeOff /> : <FiEye />}
              </span>
            </div>
            <div className="password-wrapper">
              <input
                type={showPassword ? "text" : "password"}
                id="password"
                placeholder="Masukkan Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>
          <button type="submit" className="login-btn">
            Log in
          </button>
        </form>
        <p className="forgot-password">Forget your password</p>
      </div>
    </div>
  );
};

export default Login;

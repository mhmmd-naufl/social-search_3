import React, { useState } from "react";
import { Link } from "react-router-dom"; // Import Link dari react-router-dom
import { FaHome, FaSearch, FaUser, FaBook, FaSignOutAlt } from "react-icons/fa"; // Import ikon dari react-icons
import './Sidebar.css'; // Import file CSS terpisah

const Sidebar = ({ children }) => {
  const [isOpen, setIsOpen] = useState(true); // State untuk mengontrol sidebar

  const toggleSidebar = () => {
    setIsOpen(!isOpen); // Toggle visibilitas sidebar
  };

  return (
    <div style={{ display: "flex" }}>
      {/* Sidebar */}
      <div className={`sidebar ${isOpen ? "" : "closed"}`}>
        {isOpen && (
          <>
            <div className="sidebar-header">
              <img
                src="/assets/logo+teks.png" // Ganti dengan path logo kamu
                alt="Logo"
              />
            </div>

            <div className="sidebar-menu">
              <h3>Menu</h3>
              <ul>
                <li>
                  <Link to="/dashboard">
                    <FaHome style={{ marginRight: "10px" }} /> Dashboard Utama
                  </Link>
                </li>
                <li>
                  <Link to="/pencarian-konten">
                    <FaSearch style={{ marginRight: "10px" }} /> Pencarian Konten
                  </Link>
                </li>
                <li>
                  <Link to="/Pantau-Akun">
                    <FaUser style={{ marginRight: "10px" }} /> Pantau Akun
                  </Link>
                </li>
                <li>
                  <Link to="/pustaka-makna">
                    <FaBook style={{ marginRight: "10px" }} /> Pustaka Makna
                  </Link>
                </li>
              </ul>
            </div>

            <div className="sidebar-footer">
              <Link to="/login">
                <FaSignOutAlt style={{ marginRight: "10px" }} /> Keluar
              </Link>
            </div>
          </>
        )}
      </div>

      {/* Tombol Toggle Sidebar */}
      <button
        onClick={toggleSidebar}
        className={`toggle-button ${isOpen ? "" : "closed"}`}
      >
        {isOpen ? "<" : ">"}
      </button>

      {/* Konten Halaman */}
      <div className={`content ${isOpen ? "" : "closed"}`}>
        {children}
      </div>
    </div>
  );
};

export default Sidebar;

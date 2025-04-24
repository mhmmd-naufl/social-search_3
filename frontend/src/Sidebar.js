import React, { useState } from "react";
import { Link } from "react-router-dom"; // Import Link dari react-router-dom

const Sidebar = ({ children }) => {
  const [isOpen, setIsOpen] = useState(true); // State untuk mengontrol sidebar

  const toggleSidebar = () => {
    setIsOpen(!isOpen); // Toggle visibilitas sidebar
  };

  return (
    <div style={{ display: "flex" }}>
      {/* Sidebar */}
      <div
        style={{
          width: isOpen ? "250px" : "0",
          height: "100vh",
          backgroundColor: "#0B365F",
          color: "white",
          overflow: "hidden",
          transition: "width 0.3s ease",
          position: "fixed",
          top: 0,
          left: 0,
          display: "flex",
          flexDirection: "column",
          padding: isOpen ? "20px" : "0",
        }}
      >
        {isOpen && (
          <>
            <h3 style={{ textAlign: "center", borderBottom: "1px solid #34495e", paddingBottom: "10px" }}>
              Menu
            </h3>
            <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
              <li
                style={{
                  margin: "10px 0",
                  height: "40px",
                  display: "flex",
                  alignItems: "center",
                  borderRadius: "5px",
                  transition: "background-color 0.3s ease",
                }}
                onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#4072A4")}
                onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
              >
                <Link
                  to="/dashboard"
                  style={{
                    textDecoration: "none",
                    color: "white",
                    fontSize: "16px",
                    padding: "0 15px",
                    width: "100%",
                    height: "100%",
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  Dashboard Utama
                </Link>
              </li>
              <li
                style={{
                  margin: "10px 0",
                  height: "40px",
                  display: "flex",
                  alignItems: "center",
                  borderRadius: "5px",
                  transition: "background-color 0.3s ease",
                }}
                onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#4072A4")}
                onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
              >
                <Link
                  to="/pencarian-konten"
                  style={{
                    textDecoration: "none",
                    color: "white",
                    fontSize: "16px",
                    padding: "0 15px",
                    width: "100%",
                    height: "100%",
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  Pencarian Konten
                </Link>
              </li>
              <li
                style={{
                  margin: "10px 0",
                  height: "40px",
                  display: "flex",
                  alignItems: "center",
                  borderRadius: "5px",
                  transition: "background-color 0.3s ease",
                }}
                onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#4072A4")}
                onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
              >
                <Link
                  to="Pantau-Akun"
                  style={{
                    textDecoration: "none",
                    color: "white",
                    fontSize: "16px",
                    padding: "0 15px",
                    width: "100%",
                    height: "100%",
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  Pantau Akun
                </Link>
              </li>
              <li
                style={{
                  margin: "10px 0",
                  height: "40px",
                  display: "flex",
                  alignItems: "center",
                  borderRadius: "5px",
                  transition: "background-color 0.3s ease",
                }}
                onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#4072A4")}
                onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
              >
                <Link
                  to="/pustaka-makna"
                  style={{
                    textDecoration: "none",
                    color: "white",
                    fontSize: "16px",
                    padding: "0 15px",
                    width: "100%",
                    height: "100%",
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  Pustaka Makna
                </Link>
              </li>
              <li
                style={{
                  position: "absolute", // Posisi absolut
                  bottom: "40px", // Jarak dari bawah
                  left: "0", // Jarak dari kiri
                  width: "100%", // Lebar penuh
                  height: "40px", // Tinggi tombol
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  borderRadius: "5px",
                  transition: "background-color 0.3s ease",
                  cursor: "pointer",
                }}
                onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#D32F2F")}
                onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "transparent")}
              >
                <Link
                  to="/keluar"
                  style={{
                    textDecoration: "none",
                    color: "white",
                    fontSize: "16px",
                    padding: "0 15px",
                    width: "100%",
                    height: "100%",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  Keluar
                </Link>
              </li>
            </ul>
          </>
        )}
      </div>

      {/* Tombol Toggle Sidebar */}
      <button
        onClick={toggleSidebar}
        style={{
          position: "fixed",
          top: "20px",
          left: isOpen ? "250px" : "10px",
          backgroundColor: "#4072A4",
          color: "white",
          border: "none",
          padding: "10px 15px",
          cursor: "pointer",
          borderRadius: "5px",
          fontSize: "14px",
          transition: "left 0.3s ease, background-color 0.3s ease",
        }}
      >
        {isOpen ? "<" : ">"}
      </button>

      {/* Konten Halaman */}
      <div
        style={{
          marginLeft: isOpen ? "250px" : "0",
          padding: "20px",
          width: "100%",
          transition: "margin-left 0.3s ease",
        }}
      >
        {children}
      </div>
    </div>
  );
};

export default Sidebar;
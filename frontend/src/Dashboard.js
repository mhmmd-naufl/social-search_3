import React, { useState, useEffect } from "react";
import "./Dashboard.css";
import {
  FaSun,
  FaCalendarAlt,
  FaClock,
  FaFileAlt,
  FaChevronDown,
} from "react-icons/fa";

const Dashboard = () => {
  const [weather, setWeather] = useState(null);
  const [language, setLanguage] = useState("id"); // Default bahasa Indonesia
  const [userName, setUserName] = useState("Ms. Safa");

  useEffect(() => {
    const fetchWeather = async () => {
      const apiKey = "39699f61db3b4088483dff28ef6f48ab"; // ← ganti dengan API key kamu
      const city = "Banyuwangi";
      const response = await fetch(
        `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`
      );
      const data = await response.json();
      setWeather({
        temp: data.main.temp,
        description: data.weather[0].description,
      });
    };

    fetchWeather(); // panggil saat komponen pertama kali render
    const interval = setInterval(fetchWeather, 10 * 60 * 1000); // update tiap 10 menit
    return () => clearInterval(interval); // bersihkan interval saat unmount
  }, []);

  const toggleLanguage = (lang) => {
    setLanguage(lang);
  };

  // === CALENDAR ===
  const today = new Date();
  const dayNames = [
    "Minggu",
    "Senin",
    "Selasa",
    "Rabu",
    "Kamis",
    "Jumat",
    "Sabtu",
  ];
  const dayName = dayNames[today.getDay()];
  const date = today.toLocaleDateString("id-ID", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  // === CLOCK ===
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setTime(new Date());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="dashboard-container">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h2>VIBEANALYSIS</h2>
        </div>
        <ul className="sidebar-menu">
          <li>Dashboard Utama</li>
          <li>Pustaka Makna</li>
          <li>Pencarian Konten</li>
          <li>Pantau Akun</li>
        </ul>
      </aside>
      <main className="main-content">
        <div className="welcome-section">
          <h1>Selamat Datang, Ms. Safa!</h1>
          <p className="dashboard-subtitle">Dashboard Utama</p>
        </div>
        <div className="activity-summary">
          <div className="activity-header">
            <h3 className="activity-title">Ringkasan Aktivitas</h3>

            <div className="update-info-card">
              <div className="update-text">
                <span>Data Terakhir Diperbarui: 15 Juli 2024</span>
                <FaChevronDown className="dropdown-icon" />
              </div>
            </div>
          </div>

          <div className="cards-container">
            {/* Kartu besar Banyuwangi */}
            <div className="weather-section">
              <div className="card weather-card">
                <FaSun size={86} className="card-icon-bwi" />
                <h4>BANYUWANGI</h4>
                {weather ? (
                  <p>
                    {weather.temp}°C - {weather.description}
                  </p>
                ) : (
                  <p>Loading...</p>
                )}
              </div>
            </div>

            {/* Kartu kecil kanan */}
            <div className="small-cards-section">
              <div className="top-small-cards">
                <div className="card date-card">
                  <FaCalendarAlt size={50} className="card-icon-tanggal" />
                  <h4>{dayName}</h4>
                  <p>{date}</p>
                </div>

                <div className="card time-card">
                  <FaClock size={50} className="card-icon-pukul" />
                  <h4>Pukul</h4>
                  {time.toLocaleTimeString("id-ID", {
                    hour: "2-digit",
                    minute: "2-digit",
                    hour12: false,
                  })}{" "}
                  WIB
                </div>
              </div>

              {/* Baris 2: Jumlah Kata */}
              <div className="bottom-small-card">
                <div className="card word-count-card">
                  <div className="word-count-content">
                    <FaFileAlt size={50} className="card-icon-left" />
                    <div>
                      <h4>JUMLAH KATA</h4>
                      <p>820 KATA</p>
                    </div>
                    <button className="check-button">Cek Disini</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>{" "}
        {/* penutup activity-summary */}
      </main>{" "}
      {/* penutupds main-content */}
    </div>
  );
};

export default Dashboard;

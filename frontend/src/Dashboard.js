import React, {useState } from "react";
import Sidebar from "./Sidebar";
import "./Dashboard.css";

const Dashboard = () => {
  const [data, setData] = useState(null);

  return (
    <Sidebar>
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h1>Dashboard Admin</h1>
          <h2>Selamat Datang, Admin!</h2>
          <p>Ini adalah halaman dashboard utama Anda.</p>
        </div>

        <div className="dashboard-content">
          <div className="card">
            <h4>Statistik Singkat</h4>
            <p>Total laporan yang masuk hari ini: 12</p>
          </div>

          <div className="card">
            <h4>Aktivitas Terbaru</h4>
            <p>Admin telah memverifikasi 3 laporan berita hoaks.</p>
          </div>

          <div className="card">
            <h4>Data dari API</h4>
            <p>{data ? data.message : "Memuat data..."}</p>
          </div>
        </div>
      </div>
    </Sidebar>
  );
};

export default Dashboard;
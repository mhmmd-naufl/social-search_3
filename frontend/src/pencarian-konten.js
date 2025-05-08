import React, { useState } from "react";
import axios from "axios";
import "./pencarian-konten.css";
import Sidebar from "./Sidebar";

function PencarianKonten() {
  const [keyword, setKeyword] = useState("");
  const [hasil, setHasil] = useState([]);

  const handleSearch = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/search", {
        params: { keyword },
      });
      setHasil(response.data.data);
    } catch (error) {
      console.error("Gagal mencari konten:", error);
    }
  };

  return (
    <Sidebar>
      <div className="body">
        <div className="container">
          <div className="search-bar">
            <input
              type="text"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              placeholder="Cari konten TikTok..."
            />
            <button onClick={handleSearch}>Cari</button>
          </div>

          <div className="result-list">
            {hasil.map((item) => (
              <div key={item.video_id} className="result-card">
                <a href={item.url} target="_blank" rel="noopener noreferrer">
                  {item.desc}
                </a>
                <p>Oleh: @{item.nickname}</p>
                <p>
                  {item.jumlah_comment} komentar • {item.tanggal_upload}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Sidebar>
  );
}

export default PencarianKonten;

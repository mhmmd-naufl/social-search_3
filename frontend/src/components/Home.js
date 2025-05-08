import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";

function Home() {
  const [keyword, setKeyword] = useState("");
  const navigate = useNavigate();

  const handleSearch = () => {
    if (keyword.trim()) {
      navigate(`/hasil?keyword=${encodeURIComponent(keyword)}`);
    }
  };

  return (
    <div className="main">
      <div className="title">Social Search</div>
      <div className="search-bar">
        <input
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="Cari konten TikTok..."
        />
        <button onClick={handleSearch}>Cari</button>
      </div>
    </div>
  );
}

export default Home;

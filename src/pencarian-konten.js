import React, { useState } from "react";
import Sidebar from "./Sidebar";
import "./pencarian-konten.css";

const PencarianKonten = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [platform, setPlatform] = useState("instagram"); // Default platform
  const [results, setResults] = useState([]); // Simpan hasil pencarian

  const handleSearch = () => {
    if (!searchTerm) {
      alert("Masukkan kata kunci pencarian!");
      return;
    }

    // Simulasi data hasil pencarian
    const dummyResults = [
      {
        id: 1,
        description: "Halal Bihalal Kepala Desa Se kabupaten Banyuwangi. Tingkatkan persatuan dan kebersamaan antar kepala desa.",
        platform: "instagram",
        sentiment: "positif",
        image: "/assets/logo-TT.jpg",
        comments: [
          { text: "Luar biasa keren banget, semoga makin solid antar desa!", sentiment: "positif" },
          { text: "Semangat terus para pemimpin daerah kita!", sentiment: "positif" },
          { text: "Kurang lengkap tanpa acara hiburan", sentiment: "negatif" },
          { text: "Acara ini sangat bermanfaat bagi masyarakat", sentiment: "positif" },
          { text: "Kayaknya tiap tahun sama aja deh, kurang inovatif", sentiment: "negatif" },
        ],
        chartData: { positif: 60, negatif: 30, netral: 10 },
      },
      {
        id: 2,
        description: "Acara ini kurang menarik. Seharusnya ada lebih banyak inovasi untuk menarik perhatian masyarakat.",
        platform: "instagram",
        sentiment: "negatif",
        image: "/assets/logo-TT.jpg",
        comments: [
          { text: "Acara ini kurang menarik", sentiment: "negatif" },
          { text: "Seharusnya ada lebih banyak inovasi", sentiment: "negatif" },
          { text: "Bagus sih, tapi kurang promosi", sentiment: "netral" },
          { text: "Acara ini sangat bermanfaat bagi masyarakat", sentiment: "positif" },
          { text: "Kurang lengkap tanpa acara hiburan", sentiment: "negatif" },
        ],
        chartData: { positif: 20, negatif: 70, netral: 10 },
      },
    ];

    setResults(dummyResults);
  };

  return (
    <Sidebar>
      <div className="pencarian-konten-page">
        <h2>Pencarian Konten</h2>
        <div className="search-box">
          <input
            type="text"
            placeholder="Cari Konten"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <select
            value={platform}
            onChange={(e) => setPlatform(e.target.value)}
          >
            <option value="instagram">Instagram</option>
            <option value="tiktok">TikTok</option>
          </select>
          <button onClick={handleSearch}>Cari</button>
        </div>

        <div className="results">
          {results.map((result) => (
            <div
              key={result.id}
              className={`result-card ${result.sentiment}`}
            >
              {/* Tampilkan gambar atau thumbnail */}
              <img
                src={result.image}
                alt="Post Thumbnail"
                className="post-thumbnail"
              />
              <p className="description">{result.description}</p>
              <div className="comments">
                <h4>Cuplikan Komentar</h4>
                <ul>
                  {result.comments.map((comment, index) => (
                    <li key={index}>
                      {comment.text} — <span className={comment.sentiment}>{comment.sentiment}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="chart">
                <h4>Diagram Sentimen</h4>
                <div
                  className="pie-chart"
                  style={{
                    "--value-positif": result.chartData.positif,
                    "--value-negatif": result.chartData.negatif,
                    "--value-netral": result.chartData.netral,
                  }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </Sidebar>
  );
};

export default PencarianKonten;
import React, { useState } from "react";
import Sidebar from "./Sidebar";
import "./pencarian-konten.css";
import vader from "vader-sentiment"; // AI SENTIMEN ANALYZER

const PencarianKonten = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [platform, setPlatform] = useState("instagram");
  const [results, setResults] = useState([]);

  // AI ANALISIS KOMENTAR MENGGUNAKAN VADER
  const analyzeSentiment = (text) => {
    const result = vader.SentimentIntensityAnalyzer.polarity_scores(text);
    if (result.compound >= 0.05) return "positif";
    if (result.compound <= -0.05) return "negatif";
    return "netral";
  };

  const calculateChartData = (comments) => {
    const sentimentCount = { positif: 0, negatif: 0, netral: 0 };
    comments.forEach((comment) => {
      sentimentCount[comment.sentiment]++;
    });
    const total = comments.length;
    return {
      positif: (sentimentCount.positif / total) * 100,
      negatif: (sentimentCount.negatif / total) * 100,
      netral: (sentimentCount.netral / total) * 100,
    };
  };

  const handleSearch = () => {
    if (!searchTerm) {
      alert("Masukkan kata kunci pencarian!");
      return;
    }

    // Dummy data sementara
    const dummyResults = [
      {
        id: 1,
        username: "@kominfobanyuwangi",
        description: "Halal Bihalal Kepala Desa Se kabupaten Banyuwangi.",
        platform: "instagram",
        image: "/assets/postingan1.jpg",
        comments: [
          { text: "Luar biasa keren banget, semoga makin solid antar desa!" },
          { text: "Semangat terus para pemimpin daerah kita!" },
          { text: "formalitas kegiatan" },
          { text: "Acara ini sangat bermanfaat bagi masyarakat" },
          { text: "Kayaknya tiap tahun sama aja deh, kurang inovatif" },
        ],
      },
      {
        id: 2,
        username: "@disparbanyuwangi",
        description: "Bagi bagi sembako untuk masyarakat yang membutuhkan.",
        platform: "instagram",
        image: "/assets/postingan2.jpg",
        comments: [
          { text: "kurang fuckyou yang menerima" },
          { text: "Seharusnya shit lebih banyak inovasi" },
          { text: "Bagus sih, terima " },
          { text: "Acara ini sangat bermanfaat bagi masyarakat" },
          { text: "Kok itu itu aja yang dapet haha udh dijatah sodara" },
        ],
      },
    ];

    const filteredResults = dummyResults.filter((result) => {
      const keyword = searchTerm.toLowerCase();
      const inDescription = result.description.toLowerCase().includes(keyword);
      const inUsername = result.username.toLowerCase().includes(keyword);
      const inComments = result.comments.some((comment) =>
        comment.text.toLowerCase().includes(keyword)
      );
      const matchPlatform = result.platform === platform;

      return matchPlatform && (inDescription || inUsername || inComments);
    });

    const analyzedResults = filteredResults.map((result) => {
      const analyzedComments = result.comments.map((comment) => ({
        ...comment,
        sentiment: analyzeSentiment(comment.text),
      }));
      return {
        ...result,
        comments: analyzedComments,
        chartData: calculateChartData(analyzedComments),
      };
    });

    setResults(analyzedResults);
  };

  return (
    <Sidebar>
      <div className="pencarian-konten-page">
        <h2 className="search-title">Pencarian Konten</h2>

        <div className="search-controls">
          <input
            type="text"
            placeholder="Cari konten berdasarkan deskripsi, akun, atau komentar..."
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
            <div key={result.id} className="result-card">
              <h3>{result.username}</h3>
              <img
                src={result.image}
                alt="Post Thumbnail"
                className="post-thumbnail"
              />
              <h3 className="description">{result.description}</h3>
              <div className="comments">
                <h4>Cuplikan Komentar</h4>
                <ul>
                  {result.comments.map((comment, index) => (
                    <li key={index}>
                      {comment.text} —{" "}
                      <span className={comment.sentiment}>
                        {comment.sentiment}
                      </span>
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

import React, { useState } from 'react';
import './pantau-akun.css';
import Sidebar from './Sidebar';
import { FaInstagram } from 'react-icons/fa';
import { SiTiktok } from 'react-icons/si';

function PantauAkun() {
  const [username, setUsername] = useState('');
  const [platform, setPlatform] = useState('');
  const [accountData, setAccountData] = useState(null);
  const [showAnalysis, setShowAnalysis] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const dummyAccounts = [
    {
      username: "@kominfobanyuwangi",
      name: "Diskominfo Banyuwangi",
      platform: "Instagram",
      profilePic: "./assets/kominfo.png",
      followers: "17.6K",
      posts: 809,
      comments: 423,
      address: "Jl. Agus Salim No.85 Banyuwangi",
      phone: "(0333)42400",
      commentsData: [
        { text: "@wongbwi Tingkatkan Teknologi Banyuwangi, jangan gini gini aja", sentiment: "negative" },
        { text: "@nopalpenataban Info menarik min", sentiment: "neutral" },
        { text: "@safadipsar semoga lebih baik kedepannya", sentiment: "positive" },
      ],
    },
    {
      username: "@disparbanyuwangi",
      name: "Dinas Pariwisata",
      platform: "TikTok",
      profilePic: "./assets/dispar.jpg",
      followers: "5.3K",
      posts: 230,
      comments: 112,
      address: "Jl. Raya No.1 Banyuwangi",
      phone: "(0333)55500",
      commentsData: [
        { text: "@wongpariwisata Lokasi wisata yang keren!", sentiment: "positive" },
        { text: "@tiwiparadiso Ayo liburan di Banyuwangi", sentiment: "positive" },
        { text: "@cahbanyuwangi Kurang promosinya", sentiment: "negative" },
      ],
    },
  ];

  const handleSearch = () => {
    if (!username || !platform) {
      alert("Harap isi username dan pilih platform.");
      return;
    }

    const searchInput = username.toLowerCase();
    const selectedPlatform = platform.toLowerCase();

    const foundAccount = dummyAccounts.find(acc => 
      acc.platform.toLowerCase() === selectedPlatform &&
      (acc.username.toLowerCase().includes(searchInput) || acc.name.toLowerCase().includes(searchInput))
    );

    if (foundAccount) {
      setAccountData(foundAccount);
      setShowAnalysis(false);
      setErrorMessage('');
    } else {
      setAccountData(null);
      setShowAnalysis(false);
      setErrorMessage('Akun tidak ditemukan atau data tidak sesuai.');
    }
  };

  const handleAnalyze = () => {
    if (accountData) {
      setShowAnalysis(true);
    }
  };

  const getPlatformIcon = (platform) => {
    switch (platform.toLowerCase()) {
      case "instagram":
        return <FaInstagram size={20} color="#C13584" />;
      case "tiktok":
        return <SiTiktok size={20} color="#000000" />;
      default:
        return <span role="img" aria-label="web">🌐</span>;
    }
  };

  return (
    <Sidebar>
      <div className="pantau-akun">
        <h2>Pantau Akun</h2>
        <div className="search-controls">
          <input 
            type="text" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
            placeholder="Masukkan Username Akun Anda..." 
          />
          <select value={platform} onChange={(e) => setPlatform(e.target.value)}>
            <option value="">Pilih Platform</option>
            <option value="Instagram">Instagram</option>
            <option value="TikTok">TikTok</option>
          </select>
          <button onClick={handleSearch}>Cari</button>
        </div>

        {errorMessage && <p className="error-message">{errorMessage}</p>}

        {accountData && (
          <div className="account-result">
            <div className="account-card">
              <img src={accountData.profilePic} alt="Logo Akun" />
              <div className="account-info">
                <span className="username">{accountData.username}</span>
                <h3>{accountData.name}</h3>
                <p>{accountData.address}<br />{accountData.phone}</p>
                <div className="platform">{getPlatformIcon(accountData.platform)}</div>
              </div>
              <div className="account-stats">
                <p>Followers <b>{accountData.followers}</b></p>
                <p>Postingan <b>{accountData.posts}</b></p>
                <p>Komentar <b>{accountData.comments}</b></p>
                <button onClick={handleAnalyze}>Mulai Menganalisa</button>
              </div>
            </div>

            {showAnalysis && (
              <div className="analysis-section">
                <div className="comments-box">
                  <h4>Komentar terbanyak like di akun ini</h4>
                  {accountData.commentsData.map((comment, index) => (
                    <div key={index} className="comment">{comment.text}</div>
                  ))}
                </div>
                <div className="sentiment-box">
                  <h4>Identifikasi seluruh komentar akun ini</h4>
                  <label>Positif Komentar</label>
                  <div className="bar green" style={{ width: '40%' }}>40%</div>
                  <label>Netral Komentar</label>
                  <div className="bar purple" style={{ width: '30%' }}>30%</div>
                  <label>Negatif Komentar</label>
                  <div className="bar red" style={{ width: '18%' }}>18%</div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </Sidebar>
  );
}

export default PantauAkun;

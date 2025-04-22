import React, { useState } from 'react';
import Navbar from './components/Navbar';
import SearchBar from './components/SearchBar';
import SearchResults from './components/SearchResults';
import './styles.css';

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searched, setSearched] = useState(false);

  const handleSearch = async (keyword) => {
    setLoading(true);
    setError(null);
    setSearched(true);
    
    try {
      const response = await fetch(`/api/search?keyword=${encodeURIComponent(keyword)}`);
      
      if (!response.ok) {
        throw new Error('Gagal mengambil hasil pencarian');
      }
      
      const data = await response.json();
      setResults(data.results || []);
    } catch (err) {
      console.error('Error pencarian:', err);
      setError(err.message);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <Navbar />
      <main className="main-content">
        <h2 className="app-title">Temukan konten media sosial yang sedang tren</h2>
        <p className="app-description">
          Cari konten TikTok dan Instagram hanya dengan kata kunci
        </p>
        <SearchBar onSearch={handleSearch} />
        {searched && <SearchResults results={results} loading={loading} error={error} />}
      </main>
      <footer className="footer">
        <p>ProyekSocial Search &copy; {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
}

export default App;
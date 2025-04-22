import React from 'react';
import ResultItem from './ResultItem';

function SearchResults({ results, loading, error }) {
  if (loading) {
    return <div className="loading">Mencari di platform media sosial...</div>;
  }

  if (error) {
    return <div className="error-message">Error: {error}</div>;
  }

  if (results.length === 0) {
    return <div className="no-results">Tidak ada hasil ditemukan. Coba kata kunci yang berbeda.</div>;
  }

  return (
    <div className="results-container">
      <h2 className="results-header">Hasil Pencarian ({results.length})</h2>
      <div className="results-list">
        {results.map((result, index) => (
          <ResultItem key={index} result={result} />
        ))}
      </div>
    </div>
  );
}

export default SearchResults;
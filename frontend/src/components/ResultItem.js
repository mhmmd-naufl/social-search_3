import React from 'react';

function ResultItem({ result }) {
  const { platform, title, author, url, thumbnail, likes, timestamp } = result;
  
  const platformIcon = platform === 'tiktok' 
    ? '🎵' // Ikon TikTok
    : '📷'; // Ikon Instagram

  return (
    <div className="result-item">
      {thumbnail && <img src={thumbnail} alt={title} className="result-thumbnail" />}
      <div className="result-content">
        <h3 className="result-title">
          <span className="platform-icon">{platformIcon}</span>
          <a href={url} target="_blank" rel="noopener noreferrer">{title}</a>
        </h3>
        <p className="result-author">Oleh: {author}</p>
        <div className="result-meta">
          <span className="result-likes">❤️ {likes}</span>
          <span className="result-time">{new Date(timestamp).toLocaleDateString()}</span>
          <span className="result-platform">{platform}</span>
        </div>
      </div>
    </div>
  );
}

export default ResultItem;
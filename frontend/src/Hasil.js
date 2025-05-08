import React, { useEffect, useState } from "react";
import axios from "axios";
import { useLocation } from "react-router-dom";
import "./Hasil.css";

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

function Hasil() {
  const query = useQuery();
  const keyword = query.get("keyword") || "";
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (keyword) {
      setLoading(true);
      axios
        .get(`http://localhost:8000/api/search?keyword=${keyword}`)
        .then((res) => {
          console.log(res.data.data);
          setResults(res.data.data);
          setLoading(false);
        })
        .catch((err) => {
          console.error(err);
          setLoading(false);
        });
    }
  }, [keyword]);

  return (
    <div className="container">
      <form className="search-bar" action="/hasil" method="get">
        <input
          name="keyword"
          defaultValue={keyword}
          placeholder="Cari konten TikTok..."
          aria-label="Cari konten TikTok"
        />
        <button type="submit">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <circle cx="11" cy="11" r="8" />
            <line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
          Cari
        </button>
      </form>

      {loading ? (
        <p className="loading">Sedang mencari data...</p>
      ) : (
        <div className="result-list">
          {results.length > 0 ? (
            results.map((item) => (
              <div className="result-card" key={item.video_id}>
                <a
                  href={item.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="nickname"
                >
                  {item.nickname || item.url}
                </a>
                <div className="url">
                  <p>{item.url}</p>
                </div>
                <div className="desc">
                  <p>{item.desc}</p>
                </div>
                <div className="tanggal_upload">
                  <p>Tanggal Upload: {item.tanggal_upload}</p>
                </div>
                <p>Total Komentar: {item.jumlah_comment}</p>
                <div className="comments">
                  <p>
                    <strong>Komentar:</strong>
                  </p>
                  {item.comments && item.comments.length > 0 ? (
                    <>
                      <ul className="comment-list">
                        {item.comments.slice(0, 4).map((comment, index) => (
                          <li key={index} className="comment-item">
                            {comment.text}
                          </li>
                        ))}
                      </ul>
                      {item.comments.length > 4 && (
                        <p className="more-comments">...</p>
                      )}
                    </>
                  ) : (
                    <p className="no-comments">Tidak ada komentar.</p>
                  )}
                </div>
              </div>
            ))
          ) : (
            <p>Tidak ada hasil untuk "{keyword}".</p>
          )}
        </div>
      )}
    </div>
  );
}

export default Hasil;

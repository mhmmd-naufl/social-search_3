/* eslint-env worker */
self.onmessage = function(e) {
  const { keyword, maxVideos } = e.data;
  if (!keyword) return;

  const source = new EventSource(`http://localhost:8000/search?keyword=${encodeURIComponent(keyword)}&max_videos=${maxVideos}`);

  source.onmessage = function(event) {
    try {
      const video = JSON.parse(event.data);
      self.postMessage({ type: 'result', data: video });
    } catch (err) {
      self.postMessage({ type: 'error', message: `Error parsing data: ${err.message}` });
    }
  };

  source.onerror = function() {
    self.postMessage({ type: 'error', message: 'Gagal terhubung ke server' });
    source.close();
  };

  self.onmessage = function(e) {
    if (e.data.type === 'close') {
      source.close();
    }
  };
};
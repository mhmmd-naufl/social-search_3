document.getElementById("searchAccountBtn").addEventListener("click", () => {
    const username = document.getElementById("accountUsername").value.trim();
    const platform = document.getElementById("accountPlatform").value;
  
    if (!username || !platform) {
      alert("Harap isi username dan pilih platform.");
      return;
    }
  
    // Simulasi data dari API
    const dummyData = {
      username: "@kominfobwi",
      name: "Kominfo Banyuwangi",
      profilePic: "https://upload.wikimedia.org/wikipedia/commons/9/97/Smart_Kampung_Logo.png",
      categories: ["Pelayanan", "Pemerintah"],
      engagementRate: "12%",
      followers: "125.6K",
      platform: platform,
    };
  
    renderAccountCard(dummyData);
  });
  
  function renderAccountCard(data) {
    const container = document.getElementById("accountResult");
    container.innerHTML = `
      <div class="account-card">
        <img src="${data.profilePic}" alt="Logo Akun" />
        <div class="account-info">
          <span>${data.username}</span>
          <h3>${data.name}</h3>
          ${data.categories.map(cat => `<span class="badge">${cat}</span>`).join(" ")}
          <div class="platform-icon">${getPlatformIcon(data.platform)} ${data.platform}</div>
        </div>
        <div class="account-stats">
          <div class="engagement">❤️ Engagement ${data.engagementRate}</div>
          <div class="followers">👁️ Followers ${data.followers}</div>
          <button id="analyzeBtn">Mulai Menganalisa</button>
        </div>
      </div>
    `;
  
    document.getElementById("analyzeBtn").addEventListener("click", () => {
      alert(`Menganalisa akun ${data.username} di platform ${data.platform}`);
    });
  }
  
  function getPlatformIcon(platform) {
    switch (platform.toLowerCase()) {
      case "instagram":
        return "📷";
      case "twitter":
        return "🐦";
      case "facebook":
        return "📘";
      default:
        return "🌐";
    }
  }
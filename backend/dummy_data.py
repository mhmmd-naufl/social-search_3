def dummy_search(keyword: str):
    dummy_results = [
        {
            "platform": "TikTok",
            "title": f"Contoh video tentang {keyword}",
            "link": f"https://www.tiktok.com/@dummy/video/{hash(keyword)%10000}",
            "sentiment": "positive"
        },
        {
            "platform": "Instagram",
            "title": f"{keyword} menjadi tren terbaru!",
            "link": f"https://www.tiktok.com/@dummy/video/{hash(keyword)%9999}",
            "sentiment": "neutral"
        }
    ]
    return dummy_results
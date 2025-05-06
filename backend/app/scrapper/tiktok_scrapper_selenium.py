# import json
import requests
from datetime import datetime
from db.mongodb import search_collection
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_new_cookies():
    options = Options()
    options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service("C:/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.tiktok.com/")
        print("Navigasi ke TikTok berhasil.")

        cookies = driver.get_cookies()
        cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
        print("Cookies berhasil diambil.")
        return cookie_str
    finally:
        driver.quit()

async def search_videos_by_keyword(keyword, max_videos=20):
    cookies = get_new_cookies()

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.8",
        "cookie": cookies,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "referer": "https://www.tiktok.com/",
    }

    video_ids = []
    cursor = 0
    has_more = True

    while has_more and len(video_ids) < max_videos:
        url = (
            f"https://www.tiktok.com/api/search/general/full/?"
            f"aid=1988&app_language=en&app_name=tiktok_web&browser_language=en-US&"
            f"browser_name=Mozilla&browser_online=true&browser_platform=Win32&"
            f"browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20"
            f"AppleWebKit%2F537.36%20%28KHTML%2C%20Gecko%29%20Chrome%2F135.0.0.0%20"
            f"Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=30&"
            f"cursor={cursor}&device_platform=web_pc&focus_state=true&from_page=search&"
            f"history_len=3&is_fullscreen=false&is_page_visible=true&keyword={keyword}&"
            f"os=windows&priority_region=®ion=ID&screen_height=1050&screen_width=1680&"
            f"tz_name=Asia%2FJakarta&user_is_login=false"
        )

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                raw_data = response.json()

                videos = raw_data.get("data", [])
                for item in videos:
                    if item.get("type") == 1:
                        video_id = item.get("item", {}).get("id")
                        nickname = item.get("item", {}).get("author", {}).get("nickname")
                        jumlah_comment = item.get("item", {}).get("stats", {}).get("commentCount")
                        desc = item.get("item", {}).get("desc")
                        kode_tanggal = item.get("item", {}).get("createTime")
                        object_tanggal = datetime.fromtimestamp(kode_tanggal)
                        tanggal = object_tanggal.strftime("%d-%m-%Y")

                        if video_id:
                            video_url = f"https://www.tiktok.com/@{nickname}/video/{video_id}"
                            data_video = {
                                "video_id": video_id,
                                "url": video_url,
                                "desc": desc,
                                "tanggal": tanggal,
                                "nickname": nickname,
                                "jumlah_comment": jumlah_comment,
                                "keyword": keyword
                            }
                            video_ids.append(data_video)
                            await save_to_mongo(data_video)

                has_more = raw_data.get("has_more", False)
                cursor = raw_data.get("cursor", cursor + 30)

                print(f"Fetched {len(videos)} videos, next cursor: {cursor}")

        except Exception as e:
            print(f"Error saat mengambil data: {e}")
            has_more = False

    print(f"Scraping data untuk keyword: {keyword}")
    return video_ids

async def save_to_mongo(data: dict):
    video_id = data.get("video_id")
    if not video_id:
        print("Data tidak memiliki video_id, tidak disimpan.")
        return
    try:
        await search_collection.update_one(
            {"video_id": video_id},
            {
                "$set": {
                    "platform": "tiktok",
                    "keyword": data.get("keyword", ""),
                    "url": data.get("url", ""),
                    "desc": data.get("desc", ""),
                    "tanggal_upload": data.get("tanggal", ""),
                    "nickname": data.get("nickname", ""),
                    "jumlah_comment": data.get("jumlah_comment", 0),
                    "timestamp": datetime.now()
                }
            },
            upsert=True
            )
    except Exception as e:
        print(f"Error saat menyimpan ke MongoDB: {e}")

# async def main():
#     keyword = "api"
#     max_videos = 50
#     video_ids = await search_videos_by_keyword(keyword, max_videos)
#     print("\nHasil Video TikTok:")
#     hasil = []
#     for video in video_ids:
#         hasil.append({
#             "video_id": video["video_id"],
#             "desc": video["desc"],
#             "tanggal_upload": video.get("tanggal", "N/A"),
#             "nickname": video.get("nickname", "N/A"),
#             "jumlah_comment": video.get("jumlah_comment", "N/A"),
#         })

#     print(json.dumps(hasil, indent=4, ensure_ascii=False))

# if __name__ == "__main__":
#     asyncio.run(main())

'''
List fitur yang belum :
- setelah beberapa percobaan masih bisa get 12 video
- belum dapat multiple keyword
'''
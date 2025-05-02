import requests
import json
import asyncio
import random
from playwright.async_api import async_playwright
from datetime import datetime
from ...db.mongodb import search_collection

async def get_new_cookies():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.tiktok.com/", timeout=60000)

        cookies = await page.context.cookies()
        cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

        await browser.close()
        return cookie_str

async def search_videos_by_keyword(keyword, max_videos=20):
    cookies = await get_new_cookies()

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
            f"AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F135.0.0.0%20"
            f"Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=30&"
            f"cursor={cursor}&device_platform=web_pc&focus_state=true&from_page=search&"
            f"history_len=3&is_fullscreen=false&is_page_visible=true&keyword={keyword}&"
            f"os=windows&priority_region=&region=ID&screen_height=1050&screen_width=1680&"
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

                        if video_id:
                            object_tanggal = datetime.fromtimestamp(kode_tanggal)
                            tanggal = object_tanggal.strftime("%d-%m-%Y")
                            video_url = f"https://www.tiktok.com/@{nickname}/video/{video_id}"
                            data_video = {
                                "video_id": video_id,
                                "url": video_url,
                                "desc": desc,
                                "tanggal": tanggal,
                                "nickname": nickname,
                                "jumlah_comment": jumlah_comment
                            }
                
                await save_to_mongo(data_video)
                video_ids.append(data_video)
                
                has_more = raw_data.get("has_more", False)
                cursor = raw_data.get("cursor", cursor + 30)

                print(f"Fetched {len(videos)} videos, next cursor: {cursor}")

                await asyncio.sleep(random.uniform(0.5, 2))

            else:
                print(f"Error: Gagal mengambil data (Status: {response.status_code})")
                has_more = False

        except Exception as e:
            print(f"Error saat mengambil data: {e}")
            has_more = False

    if video_ids:
        with open("tiktok_video_ids.json", "w", encoding="utf-8") as f:
            json.dump(video_ids, f, ensure_ascii=False, indent=4)
        print(f"Total {len(video_ids)} ID video berhasil disimpan ke tiktok_video_ids.json")
    else:
        print("Tidak ada video ditemukan untuk kata kunci tersebut.")

    return video_ids

async def save_to_mongo(data: dict):
    post_id = data.get("video_id")
    if not post_id:
        print("Data tidak memiliki video_id, tidak disimpan.")
        return

    try:
        await search_collection.update_one(
            {"post_id": post_id},
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
        print(f"Berhasil menyimpan data")
    except Exception as e:
        print(f"Error saat menyimpan ke MongoDB: {e}")

async def main():
    keyword = "informatika"
    max_videos = 50
    video_ids = await search_videos_by_keyword(keyword, max_videos)
    print("\nHasil Video TikTok:")
    hasil = []
    for video in video_ids:
        hasil.append({
            "video_id": video["video_id"],
            "desc": video["desc"],
            "tanggal_upload": video.get("tanggal", "N/A"),
            "nickname": video.get("nickname", "N/A"),
            "jumlah_comment": video.get("jumlah_comment", "N/A"),
        })
    
    print(json.dumps(hasil, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())

'''
List fitur yang belum :
- menyimpan di database
- setelah beberapa percobaan masih bisa get 12 video
- belum dapat multiple keyword
'''
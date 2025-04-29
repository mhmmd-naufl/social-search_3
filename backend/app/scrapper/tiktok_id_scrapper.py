import requests
import json
import asyncio
import random
from playwright.async_api import async_playwright

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

    # Opsi proxy (jika diperlukan, uncomment dan sesuaikan)
    # proxies = {
    #     'http': 'http://192.168.1.1:8080',
    #     'https': 'http://192.168.1.1:8080'
    # }

    video_ids = []
    cursor = 0
    has_more = True

    while has_more and len(video_ids) < max_videos:
        # URL API pencarian TikTok (sesuaikan parameter berdasarkan observasi)
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
            # Tambahkan proxies=proxies di bawah jika menggunakan proxy
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                raw_data = response.json()

                # Ambil video dari respons
                videos = raw_data.get("data", [])
                for item in videos:
                    if item.get("type") == 1:  # Type 1 biasanya video
                        video_id = item.get("item", {}).get("id")
                        if video_id:
                            video_ids.append({"video_id": video_id, "url": f"https://www.tiktok.com/@user/video/{video_id}"})
                            print(f"Found video ID: {video_id}")

                # Periksa apakah ada halaman berikutnya
                has_more = raw_data.get("has_more", False)
                cursor = raw_data.get("cursor", cursor + 30)

                print(f"Fetched {len(videos)} videos, next cursor: {cursor}")

                # Jeda acak untuk menghindari deteksi anti-bot
                await asyncio.sleep(random.uniform(0.5, 2))

            else:
                print(f"Error: Gagal mengambil data (Status: {response.status_code})")
                has_more = False

        except Exception as e:
            print(f"Error saat mengambil data: {e}")
            has_more = False

    # Simpan hasil ke file JSON
    if video_ids:
        with open("tiktok_video_ids.json", "w", encoding="utf-8") as f:
            json.dump(video_ids, f, ensure_ascii=False, indent=4)
        print(f"Total {len(video_ids)} ID video berhasil disimpan ke tiktok_video_ids.json")
    else:
        print("Tidak ada video ditemukan untuk kata kunci tersebut.")

    return video_ids

async def main():
    keyword = "api"  # Ganti dengan kata kunci yang diinginkan
    max_videos = 50  # Jumlah maksimum video yang ingin diambil
    video_ids = await search_videos_by_keyword(keyword, max_videos)
    print(f"Video IDs: {video_ids}")

if __name__ == "__main__":
    asyncio.run(main())
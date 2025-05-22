import requests
import json
import asyncio
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

async def scrape_and_save():
    post_url = "https://www.tiktok.com/@frdyashputra_/video/7488988646201101575"
    post_id = post_url.split("/")[-1]
    
    cookies = await get_new_cookies()

    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.8',
        'cookie': cookies,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    }

    async def req(post_id):
        url = f'https://www.tiktok.com/api/comment/list/?WebIdLastTime=1745468006&aid=1988&app_language=en&app_name=tiktok_web&aweme_id={post_id}&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F135.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=20&cursor=0&data_collection_enabled=true&device_id=7496727975040796178&device_platform=web_pc&focus_state=true&from_page=video&history_len=3&is_fullscreen=false&is_page_visible=true&odinId=7496727857532666898&os=windows&priority_region=&referer=&region=ID&screen_height=1050&screen_width=1680&tz_name=Asia%2FJakarta&user_is_login=false&verifyFp=verify_m9uul3hy_MUW0yaqI_d9uZ_4Plw_8QPG_fZD1av698o11&webcast_language=en&msToken=oLandq46SdFmJhodB5UJy5hbm1vzXXQs8AHIBPhat_--QmQ5eD-S3M20euY5jPP8TG4o3NT3XR_hUvoATGpcP-XMqoOHqbkTSjntMyLnOUglrlgtp7bNrnfDkevTueEi4EMGusJl2tUqt69-iTbTSg==&X-Bogus=DFSzswVYyAhANSo9Cayq9y3SsZDI&X-Gnarly=M/p/wtWYD29qKpbn0td6VM7-Dj8mtlNcKF47EP3jHOnaDMCJPRuYuWt0RbRNWAUNlc19-Y/noOaTTPcDQ9ECcM/mBI2juOCBvkw9WpYNYbdsynPxGNqzBTSKPyF0mE0JrQ8EbvbPgYbSucMGHVHFUD8uhkIrsYQ6tO86Czb/sriMsF0ZswQt7a8/UMquGhV-FwKToBfVO-4JQYcl7H6sYrhUFmMLfm-TwHkymJFBbP-/x2yN/0Fn-SKz18/D/rU5NjVN0fVyaXq-'
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            raw_data = response.json()
            comments = []
            for c in raw_data.get("comments", []):
                comments.append({
                    "text": c.get("text"),
                })

            # Simpan hanya ke file JSON
            with open('output_filtered.json', 'w', encoding='utf-8') as f:
                json.dump(comments, f, ensure_ascii=False, indent=4)

            print("Data berhasil disimpan ke file JSON.")
        else:
            print("Error: Gagal mengambil data dari TikTok API")

    await req(post_id)

asyncio.run(scrape_and_save())

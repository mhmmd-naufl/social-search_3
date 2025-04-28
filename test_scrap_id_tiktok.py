import requests
import json
import asyncio
from bson import ObjectId
from ...db.mongodb import search_collection
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

async def search_videos(keyword, cookies):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.8',
        'cookie': cookies,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    }

    url = f'https://www.tiktok.com/api/search/general/full/?keyword={keyword}&count=10&offset=0&source=normal_search'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list):
            video_ids = []
            for res in result:
                data = res.get('data', {})
                for item in data.get('items', []):
                    if item.get('type') == 1:
                        video_ids.append(item['item_info']['item_id'])
            return video_ids
    else:
        print("Unexpected response format:", result)
        return []

async def scrape_comments_from_video(post_id, cookies):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.8',
        'cookie': cookies,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    }

    url = f'https://www.tiktok.com/api/comment/list/?aid=1988&count=20&cursor=0&aweme_id={post_id}&device_platform=web_pc&region=ID'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        raw_data = response.json()
        comments_list = []
        for c in raw_data.get("comments", []):
            comments_list.append({
                "text": c.get("text"),
            })

        # ➔ Format data yang disimpan (group by post_id)
        document = {
            "post_id": post_id,
            "comments": comments_list
        }

        # Save ke MongoDB (per video ID)
        await search_collection.insert_one(document)

        # Fungsi buat convert ObjectId ke str supaya bisa JSON dump
        def convert_objectid_to_str(data):
            if isinstance(data, list):
                return [convert_objectid_to_str(item) for item in data]
            elif isinstance(data, dict):
                return {key: convert_objectid_to_str(value) for key, value in data.items()}
            elif isinstance(data, ObjectId):
                return str(data)
            else:
                return data

        with open(f'output_comments_{post_id}.json', 'w', encoding='utf-8') as f:
            json.dump(convert_objectid_to_str(document), f, ensure_ascii=False, indent=4)

        print(f"Comments for post_id {post_id} berhasil disimpan.")
    else:
        print(f"Error mengambil komentar untuk {post_id}")

async def scrape_and_save():
    keyword = "fyp"  # Ganti keyword sesuai kebutuhanmu
    cookies = await get_new_cookies()

    video_ids = await search_videos(keyword, cookies)

    if not video_ids:
        print("Tidak ada video ditemukan untuk keyword tersebut.")
        return

    print("Video IDs ditemukan:", video_ids)

    for vid in video_ids:
        await scrape_comments_from_video(vid, cookies)

asyncio.run(scrape_and_save())

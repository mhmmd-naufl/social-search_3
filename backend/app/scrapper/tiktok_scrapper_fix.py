# import json
import requests
import asyncio
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from db.mongodb import search_collection


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
        id_url = (
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
            response = requests.get(id_url, headers=headers, timeout=10)

            if response.status_code == 200:
                data_id = response.json()

                videos = data_id.get("data", [])
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
                            # comments = await fetch_comments_for_videos([video_id], headers)
                            # video_comments = comments.get(video_id, [])
                            data_video = {
                                "video_id": video_id,
                                "url": video_url,
                                "desc": desc,
                                "tanggal": tanggal,
                                "nickname": nickname,
                                "jumlah_comment": jumlah_comment,
                                "keyword": keyword,
                                # "comments" : video_comments
                            }
                            video_ids.append(data_video)
                            await save_to_mongo(data_video)

                has_more = data_id.get("has_more", False)
                cursor = data_id.get("cursor", cursor + 30)

                print(f"Fetched {len(videos)} videos, next cursor: {cursor}")
                return video_ids
            
        except Exception as e:
            print(f"Error saat mengambil data: {e}")
            has_more = False
            
        # pass

    # all_comments = await fetch_comments_for_videos([video["video_id"] for video in video_ids], headers)

    # for video in video_ids:
    #     video["comments"] = all_comments.get(video["video_id"], [])

# async def fetch_comments_for_videos(video_ids, headers):
#     all_video_comments = {}

#     for video_id in video_ids:
#         print(f"Mengambil komentar untuk video_id: {video_id}")
#         cursor = 0
#         has_more = True
#         video_comments = []

#         while has_more:
#             try:
#                 comments_url = (
#                     f"https://www.tiktok.com/api/comment/list/?"
#                     f"WebIdLastTime=1745468006&aid=1988&app_language=en&app_name=tiktok_web&aweme_id={video_id}&"
#                     f"browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&"
#                     f"browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20"
#                     f"AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F135.0.0.0%20"
#                     f"Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=20&"
#                     f"cursor=0&data_collection_enabled=true&device_id=7496727975040796178&device_platform=web_pc&"
#                     f"focus_state=true&from_page=video&history_len=3&is_fullscreen=false&is_page_visible=true&"
#                     f"odinId=7496727857532666898&os=windows&priority_region=&referer=&region=ID&screen_height=1050&screen_width=1680&"
#                     f"tz_name=Asia%2FJakarta&user_is_login=false&verifyFp=verify_m9uul3hy_MUW0yaqI_d9uZ_4Plw_8QPG_fZD1av698o11&"
#                     f"webcast_language=en&msToken=oLandq46SdFmJhodB5UJy5hbm1vzXXQs8AHIBPhat_--QmQ5eD-S3M20euY5jPP8TG4o3NT3XR_hUvoATGpcP-"
#                     f"XMqoOHqbkTSjntMyLnOUglrlgtp7bNrnfDkevTueEi4EMGusJl2tUqt69-iTbTSg==&X-Bogus=DFSzswVYyAhANSo9Cayq9y3SsZDI&X-"
#                     f"Gnarly=M/p/wtWYD29qKpbn0td6VM7-Dj8mtlNcKF47EP3jHOnaDMCJPRuYuWt0RbRNWAUNlc19-"
#                     f"Y/noOaTTPcDQ9ECcM/mBI2juOCBvkw9WpYNYbdsynPxGNqzBTSKPyF0mE0JrQ8EbvbPgYbSucMGHVHFUD8uhkIrsYQ6tO86Czb/sriMsF0ZswQt7a8/"
#                     f"UMquGhV-FwKToBfVO-4JQYcl7H6sYrhUFmMLfm-TwHkymJFBbP-/x2yN/0Fn-SKz18/D/rU5NjVN0fVyaXq-"
#                 )

#                 response = requests.get(comments_url, headers=headers, timeout=10)

#                 if response.status_code == 200:
#                     data_comments = response.json()

#                     comments = [
#                         {"text": c.get("text")}
#                         for c in data_comments.get("comments", [])
#                     ]
#                     video_comments.extend(comments)

#                     has_more = data_comments.get("has_more", False)
#                     cursor = data_comments.get("cursor", 0)

#                     print(f"Fetched {len(comments)} comments for video_id {video_id}, next cursor: {cursor}")
#                     await asyncio.sleep(0.5)
#                 else:
#                     print(f"Failed to fetch comments for video_id {video_id}, status code: {response.status_code}")
#                     has_more = False

#             except Exception as e:
#                 print(f"Error saat mengambil komentar untuk video_id {video_id}: {e}")
#                 has_more = False

#         all_video_comments[video_id] = video_comments
#         print(f"Fetched comments for video_id {video_id}: {video_comments}")

#     return all_video_comments

async def save_to_mongo(data: dict):
    video_id = data.get("video_id")
    if not video_id:
        print("Data tidak memiliki video_id, tidak disimpan.")
        return
    try:
        # print(f"Komentar yang akan disimpan: {data.get('comments', [])}") 
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
                    "timestamp": datetime.now(),
                    "comments": data.get("comments", []),
                }
            },
            upsert=True
            )
    except Exception as e:
        print(f"Error saat menyimpan ke MongoDB: {e}")

# async def main():
#     keyword = input("Masukkan keyword untuk pencarian TikTok: ").strip()
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

# if __name__ == "__main__":
#     asyncio.run(main())

'''
List fitur yang belum :
- setelah beberapa percobaan masih bisa get 12 video
- belum dapat multiple keyword
'''
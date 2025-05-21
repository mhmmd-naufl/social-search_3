import requests
from datetime import datetime
from .config import SEARCH_API, COMMENTS_API, HEADERS
from .save import save_to_mongo

async def search_videos(keyword, max_videos=20, cookies="", collection=None):
    """Mencari video TikTok berdasarkan kata kunci dan simpan ke MongoDB jika collection diberikan."""
    headers = HEADERS.copy()
    headers["cookie"] = cookies
    video_ids = []
    cursor = 0
    has_more = True

    while has_more and len(video_ids) < max_videos:
        url = SEARCH_API.format(keyword=keyword, cursor=cursor)
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Gagal mengambil video, status: {response.status_code}")
                break

            data = response.json()
            videos = data.get("data", [])
            for item in videos:
                if item.get("type") == 1 and "item" in item:
                    video = parse_video_data(item["item"], keyword)
                    if video:
                        video_ids.append(video)
                        if collection is not None:
                            await save_to_mongo(collection, video)
                        if len(video_ids) >= max_videos:
                            break

            has_more = data.get("has_more", False)
            cursor = data.get("cursor", cursor + 30)
            print(f"Fetched {len(videos)} videos, total: {len(video_ids)}, cursor: {cursor}")

        except Exception as e:
            print(f"Error saat scraping video: {e}")
            break

    return video_ids

async def fetch_comments(video_id, cookies=""):
    """Mengambil komentar untuk video TikTok tertentu."""
    headers = HEADERS.copy()
    headers["cookie"] = cookies
    comments = []
    url = COMMENTS_API.format(video_id=video_id)

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            comments = [{"text": c.get("text")} for c in data.get("comments", [])]
            print(f"Fetched {len(comments)} comments for video_id {video_id}")
        else:
            print(f"Gagal mengambil komentar, status: {response.status_code}")
    except Exception as e:
        print(f"Error saat mengambil komentar: {e}")

    return comments

def parse_video_data(item, keyword):
    """Mengurai data video dari respons API."""
    video_id = item.get("id")
    if not video_id:
        return None

    nickname = item.get("author", {}).get("nickname", "")
    desc = item.get("desc", "")
    kode_tanggal = item.get("createTime", 0)
    tanggal = datetime.fromtimestamp(kode_tanggal).strftime("%d-%m-%Y")
    jumlah_comment = item.get("stats", {}).get("commentCount", 0)

    return {
        "video_id": video_id,
        "url": f"https://www.tiktok.com/@{nickname}/video/{video_id}",
        "desc": desc,
        "tanggal": tanggal,
        "nickname": nickname,
        "jumlah_comment": jumlah_comment,
        "keyword": keyword,
    }
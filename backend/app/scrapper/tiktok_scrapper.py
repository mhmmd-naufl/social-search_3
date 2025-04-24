import httpx
from bs4 import BeautifulSoup
import re

async def scrape_tiktok_details(url: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        if response.status_code != 200:
            return error_response("Gagal fetch data dari TikTok.")

        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        json_text = ""
        script_tag = soup.find("script", id="SIGI_STATE")
        if script_tag:
            json_text = script_tag.string
        else:
            for script in soup.find_all("script"):
                if "playAddr" in script.text:
                    json_text = script.text
                    break

        if not json_text:
            return error_response("Tidak ditemukan data video.")

        video_match = re.search(r'"playAddr":"([^"]+)"', json_text)
        thumb_match = re.search(r'"cover":"([^"]+)"', json_text)
        username_match = re.search(r'"uniqueId":"([^"]+)"', json_text)

        if not video_match or not thumb_match or not username_match:
            return error_response("Gagal parsing. Mungkin TikTok ubah struktur.")

        video_url = (
        video_match.group(1)
        .replace("\\u0026", "&")
        .replace("\\u002F", "/")
        .replace("u002F", "/")
        .replace("\\", "")
        )

        thumb_url = (
        thumb_match.group(1)
        .replace("u002F", "/")
        .replace("\\", "")
        )

        username = username_match.group(1)

        return {
            "video": video_url,
            "withoutWaterMark": None,
            "user": username,
            "thumb": thumb_url,
            "error": False,
            "message": None
        }

    except Exception as e:
        return error_response(str(e))

def error_response(msg):
    return {
        "video": False,
        "withoutWaterMark": False,
        "user": False,
        "thumb": False,
        "error": True,
        "message": msg
    }

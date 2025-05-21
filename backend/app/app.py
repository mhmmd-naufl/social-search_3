from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from app.scrapper.cookies import get_new_cookies
from app.scrapper.scrapper import search_videos, fetch_comments
from app.scrapper.save import save_to_mongo
from db.mongodb import search_collection
from bson import ObjectId
from datetime import datetime, date, time
import json
import logging

# Inisialisasi aplikasi
app = FastAPI()

# Konfigurasi CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fungsi bantu untuk konversi ke format JSON-serializable
def make_json_serializable(obj):
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(item) for item in obj]
    elif isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, (datetime, date, time)):
        # Gunakan format yang konsisten dengan data Anda: "dd-mm-yyyy"
        return obj.strftime("%d-%m-%Y") if isinstance(obj, (datetime, date)) else obj.isoformat()
    return obj

# Generator untuk streaming hasil pencarian
async def stream_search_results(keyword: str, max_videos: int):
    try:
        logger.info(f"Mengambil data dari MongoDB untuk kata kunci: {keyword}")
        cursor = search_collection.find({"keyword": keyword}).limit(max_videos)
        result = await cursor.to_list(length=max_videos)

        # Stream data dari MongoDB
        for video in result:
            serializable_video = make_json_serializable(video)
            yield f"data: {json.dumps(serializable_video)}\n\n"
            logger.info(f"Video dari MongoDB telah distream: {video.get('video_id')}")

        # Scraping jika data kurang dari yang diminta
        if len(result) < max_videos:
            logger.info(f"Memulai scraping video tambahan untuk kata kunci: {keyword}")
            cookies = get_new_cookies()
            if not cookies:
                error = {"status": "error", "message": "Gagal mendapatkan cookies"}
                yield f"data: {json.dumps(error)}\n\n"
                return

            videos = await search_videos(keyword, max_videos - len(result), cookies, search_collection)
            for video in videos:
                serializable_video = make_json_serializable(video)
                yield f"data: {json.dumps(serializable_video)}\n\n"
                logger.info(f"Video hasil scraping telah distream: {video.get('video_id')}")

            # Tambahkan komentar untuk 2 video pertama
            if len(videos) >= 2:
                for video in videos[:2]:
                    comments = await fetch_comments(video["video_id"], cookies)
                    if comments is not None:
                        video["comments"] = make_json_serializable(comments)
                        await save_to_mongo(search_collection, video)
                        serializable_video = make_json_serializable(video)
                        yield f"data: {json.dumps(serializable_video)}\n\n"
                        logger.info(f"Video dengan komentar telah distream: {video.get('video_id')}")

    except Exception as e:
        logger.error(f"Error selama streaming: {str(e)}")
        error = {"status": "error", "message": f"Error streaming hasil: {str(e)}"}
        yield f"data: {json.dumps(error)}\n\n"

# Endpoint streaming
@app.get("/search")
async def search(keyword: str = Query(..., description="Kata kunci untuk pencarian"), max_videos: int = Query(20, description="Jumlah maksimum video yang dikembalikan")):
    return StreamingResponse(
        stream_search_results(keyword, max_videos),
        media_type="text/event-stream"
    )

# Endpoint tes root
@app.get("/")
async def root():
    return {"message": "Server sedang berjalan"}
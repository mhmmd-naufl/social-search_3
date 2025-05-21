from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from app.scrapper.cookies import get_new_cookies
from app.scrapper.scrapper import search_videos, fetch_comments
from app.scrapper.save import save_to_mongo
from db.mongodb import search_collection
import json
import logging
from bson import ObjectId

app = FastAPI()

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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_objectid_to_str(data):
    """Convert ObjectId to string for JSON serialization."""
    if isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    return data

async def stream_search_results(keyword: str, max_videos: int):
    try:
        logger.info(f"Querying MongoDB for keyword: {keyword}")
        cursor = search_collection.find({"keyword": keyword}).limit(max_videos)
        existing_videos = await cursor.to_list(length=max_videos)
        existing_videos = convert_objectid_to_str(existing_videos)

        for video in existing_videos:
            yield f"data: {json.dumps(video)}\n\n"
            logger.info(f"Streamed video from MongoDB: {video.get('video_id')}")

        if len(existing_videos) < max_videos:
            logger.info(f"Insufficient data in MongoDB for keyword: {keyword}. Starting scraping...")
            cookies = get_new_cookies()
            if not cookies:
                yield f"data: {json.dumps({'status': 'error', 'message': 'Gagal mendapatkan cookies'})}\n\n"
                return

            videos = await search_videos(keyword, max_videos - len(existing_videos), cookies, search_collection)
            for video in videos:
                yield f"data: {json.dumps(convert_objectid_to_str(video))}\n\n"
                logger.info(f"Streamed scraped video: {video.get('video_id')}")

            if len(videos) >= 2:
                for video in videos[:2]:
                    comments = await fetch_comments(video["video_id"], cookies)
                    video["comments"] = comments
                    await save_to_mongo(search_collection, video)
                    yield f"data: {json.dumps(convert_objectid_to_str(video))}\n\n"
                    logger.info(f"Streamed video with comments: {video.get('video_id')}")

    except Exception as e:
        logger.error(f"Error during streaming: {str(e)}")
        yield f"data: {json.dumps({'status': 'error', 'message': f'Error streaming results: {str(e)}'})}\n\n"

@app.get("/search")
async def search(keyword: str = Query(...), max_videos: int = Query(20)):
    return StreamingResponse(
        stream_search_results(keyword, max_videos),
        media_type="text/event-stream"
    )
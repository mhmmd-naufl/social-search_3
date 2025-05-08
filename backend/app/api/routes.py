from fastapi import APIRouter, Query, HTTPException
from db.mongodb import search_collection
from bson import ObjectId
from app.scrapper.tiktok_scrapper import search_videos_by_keyword
import logging

router = APIRouter()

# Setup logging
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

@router.get("/search")
async def scrape_and_save(keyword: str = Query(..., description="Keyword to search for"), max_videos: int = Query(20, description="Maximum number of videos to return")):
    """
    Search videos by keyword in MongoDB. If no results are found, scrape TikTok and save to MongoDB.
    """
    try:
        # Cari di MongoDB berdasarkan keyword
        logger.info(f"Querying MongoDB for keyword: {keyword}")
        results = await search_collection.find({"keyword": keyword}).to_list(length=max_videos)
        results = convert_objectid_to_str(results)

        # Jika data ditemukan di MongoDB, kembalikan hasil
        if results:
            logger.info(f"Found {len(results)} results in MongoDB for keyword: {keyword}")
            return {"status": "success", "data": results}

        # Jika tidak ada hasil, lakukan scraping
        logger.info(f"No data found in MongoDB for keyword: {keyword}. Starting scraping...")
        video_ids = await search_videos_by_keyword(keyword, max_videos)

        # Validasi hasil scraping
        if video_ids is None or not isinstance(video_ids, list):
            logger.warning(f"Scraping returned invalid or no results for keyword: {keyword}")
            return {"status": "success", "data": [], "message": "No videos found after scraping"}

        # Validasi setiap video memiliki video_id
        valid_videos = []
        for video in video_ids:
            if not isinstance(video, dict) or "video_id" not in video:
                logger.warning(f"Invalid video data, missing video_id: {video}")
                continue
            valid_videos.append(video)

        # Jika tidak ada video valid, kembalikan respons kosong
        if not valid_videos:
            logger.warning(f"No valid videos found after validation for keyword: {keyword}")
            return {"status": "success", "data": [], "message": "No valid videos found after scraping"}

        # Simpan hasil scraping ke MongoDB
        for video in valid_videos:
            try:
                await search_collection.update_one(
                    {"video_id": video["video_id"]},
                    {"$set": video},
                    upsert=True
                )
            except Exception as e:
                logger.error(f"Failed to save video {video['video_id']} to MongoDB: {str(e)}")
                continue

        # Konversi ObjectId ke string
        results = convert_objectid_to_str(valid_videos)
        logger.info(f"Scraped and saved {len(results)} videos for keyword: {keyword}")
        return {"status": "success", "data": results}

    except Exception as e:
        logger.error(f"Error querying MongoDB or scraping: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error querying MongoDB or scraping: {str(e)}")
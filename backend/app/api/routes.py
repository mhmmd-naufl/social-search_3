from fastapi import APIRouter, Query
from db.mongodb import search_collection
from bson import ObjectId
from app.scrapper.tiktok_scrapper_selenium import search_videos_by_keyword
import asyncio

router = APIRouter()

# Fungsi untuk mengonversi ObjectId menjadi string
def convert_objectid_to_str(data):
    if isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

@router.get("/search")
async def scrape_and_save(keyword: str = Query(...), max_videos: int = 20):
    try:
        # Cari data di database berdasarkan keyword
        results = await search_collection.find({"keyword": keyword}).to_list(length=max_videos)
        print(f"Hasil query MongoDB berdasarkan keyword '{keyword}': {results}")  # Log hasil query

        # Jika data tidak ditemukan, lakukan scraping
        if not results:
            print(f"Data untuk keyword '{keyword}' tidak ditemukan di database. Memulai scraping...")
            video_ids = await search_videos_by_keyword(keyword, max_videos)
            print(f"Video IDs yang dikembalikan: {video_ids}")

            # Simpan hasil scraping ke database
            for video in video_ids:
                await search_collection.update_one(
                    {"video_id": video["video_id"]},
                    {"$set": video},
                    upsert=True
                )
            results = video_ids

        # Konversi hasil query menjadi format JSON-friendly
        result = [convert_objectid_to_str(result) for result in results]
        results = await search_collection.find({"keyword": keyword}).to_list(length=max_videos)
        return {"status": "success", "data": result}
    
    except Exception as e:
        print(f"Error querying MongoDB atau scraping: {e}")
        return {"status": "error", "message": str(e)}
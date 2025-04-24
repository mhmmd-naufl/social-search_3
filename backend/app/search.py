from datetime import datetime
from fastapi import APIRouter, Query
# from dummy_data import dummy_search
from app.sentiment import analisis_komentar
from db.mongodb import search_collection

search = APIRouter()

@search.get("/keyword")
async def search_keyword(q: str = Query(..., min_length=1)):
    mock_result = {
    "keywords": q,
    "timestamp" : datetime.now(),
    "results": [
        {
        "url": f"https://www.tiktok.com/@user/video/mock1?q={q}",
                "comments": [
                    {"text": "Ini bagus banget!", "sentiment": analisis_komentar("Ini bagus banget!")},
                    {"text": "Kurang menarik", "sentiment": analisis_komentar("Kurang menarik")},
                    {"text": "Keren", "sentiment": analisis_komentar("Keren")},
                ]
            }
        ]
    }
    
    result = await search_collection.insert_one(mock_result)
    mock_result["_id"] = str(result.inserted_id)

    return mock_result
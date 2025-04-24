from fastapi import APIRouter
from pydantic import BaseModel
from app.scrapper.tiktok_scrapper import scrape_tiktok_details

router = APIRouter()

class TikTokRequest(BaseModel):
    url: str

@router.post("/tiktok/details")
async def get_details(payload: TikTokRequest):
    return await scrape_tiktok_details(payload.url)

from datetime import datetime

async def save_to_mongo(collection, data: dict):
    video_id = data.get("video_id")
    if not video_id:
        print("Data tidak memiliki video_id, tidak disimpan.")
        return

    try:
        await collection.update_one(
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
        print(f"Data untuk video_id {video_id} tersimpan.")
    except Exception as e:
        print(f"Error saat menyimpan ke MongoDB: {e}")
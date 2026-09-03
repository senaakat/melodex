import asyncio

from fastapi import APIRouter

from app.services.ytmusic_client import get_ytmusic_client

router = APIRouter(prefix="/api/ytmusic", tags=["ytmusic"])


@router.get("/search")
async def search_song(q: str):
    yt = get_ytmusic_client()
    results = await asyncio.to_thread(yt.search, q, filter="songs", limit=5)

    return [
        {
            "videoId": item.get("videoId"),
            "title": item.get("title"),
            "artists": [a["name"] for a in item.get("artists", [])],
        }
        for item in results
    ]
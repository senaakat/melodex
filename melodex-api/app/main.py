from fastapi import FastAPI

from app.api.spotify import router as spotify_router
from app.api.ytmusic import router as ytmusic_router
app = FastAPI(title="Melodex API")
app.include_router(spotify_router)

app.include_router(ytmusic_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
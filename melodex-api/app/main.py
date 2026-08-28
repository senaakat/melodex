from fastapi import FastAPI

from app.api.spotify import router as spotify_router
app = FastAPI(title="Melodex API")
app.include_router(spotify_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
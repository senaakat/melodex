from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from spotipy import Spotify

from app.core.security import decrypt_token, encrypt_token
from app.db.session import get_db
from app.models.user import User
from app.services.spotify_client import build_spotify_oauth

router = APIRouter(prefix="/api/spotify", tags=["spotify"])


@router.get("/login")
async def spotify_login():
    oauth = build_spotify_oauth()
    auth_url = oauth.get_authorize_url()
    return RedirectResponse(auth_url)


@router.get("/callback")
async def spotify_callback(code: str, db: AsyncSession = Depends(get_db)):
    oauth = build_spotify_oauth()
    token_info = oauth.get_access_token(code, as_dict=True)

    access_token = token_info["access_token"]
    refresh_token = token_info["refresh_token"]
    expires_at = datetime.fromtimestamp(token_info["expires_at"], tz=timezone.utc)

    sp = Spotify(auth=access_token)
    profile = sp.me()
    email = profile["email"]

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(email=email)
        db.add(user)

    user.spotify_access_token = encrypt_token(access_token)
    user.spotify_refresh_token = encrypt_token(refresh_token)
    user.spotify_token_expires_at = expires_at

    await db.commit()

    return {"status": "connected", "email": email}

@router.get("/playlists")
async def get_playlists(email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is None or user.spotify_access_token is None:
        return {"error": "user not connected to Spotify"}

    access_token = decrypt_token(user.spotify_access_token)
    sp = Spotify(auth=access_token)

    playlists = sp.current_user_playlists()

    return [
        {
            "id": item["id"],
            "name": item["name"],
            "track_count": item.get("tracks", {}).get("total", 0),
        }
        for item in playlists["items"]
        if item is not None
    ]
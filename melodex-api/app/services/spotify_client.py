from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from app.core.config import settings

SCOPE = "playlist-read-private playlist-read-collaborative user-read-email"

def build_spotify_oauth() -> SpotifyOAuth:
    return SpotifyOAuth(
        client_id=settings.spotify_client_id,
        client_secret=settings.spotify_client_secret,
        redirect_uri=settings.spotify_redirect_uri,
        scope=SCOPE,
    )


def get_spotify_client(access_token: str) -> Spotify:
    return Spotify(auth=access_token)
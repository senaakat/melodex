from ytmusicapi import YTMusic

from app.core.config import settings


def get_ytmusic_client() -> YTMusic:
    return YTMusic(settings.ytmusic_oauth_path)

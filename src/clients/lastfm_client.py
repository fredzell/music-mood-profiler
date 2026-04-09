import requests
from typing import Any, Dict

class LastFMClient:
    BASE_URL = "http://ws.audioscrobbler.com/2.0/"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def _get(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Shared method to make requests to the Last.fm API."""
        params = {
            **params,
            "api_key": self.api_key,
            "format": "json"
        }
   
        response = requests.get(self.BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def get_recent_tracks_page(
        self,
        user: str,
        page: int = 1,
        limit: int = 200,
        from_ts: int | None = None,
        to_ts: int | None = None,
    ) -> Dict[str, Any]:
        """Fetch a page of recent tracks for a user."""
        params = {
            "method": "user.getrecenttracks",
            "user": user,
            "page": page,
            "limit": limit,
        }
        if from_ts:
            params["from"] = from_ts
        if to_ts:
            params["to"] = to_ts
        
        return self._get(params)

if __name__ == "__main__":
    from src.config import LASTFM_API_KEY
    
    client = LastFMClient(api_key=LASTFM_API_KEY)
    
    data = client.get_recent_tracks_page(user="fredzell", limit=5)
    
    tracks = data["recenttracks"]["track"]
    
    for t in tracks:
        print(t["artist"]["#text"], "-", t["name"])
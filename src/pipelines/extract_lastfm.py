from src.clients.lastfm_client import LastFMClient
from src.config import LASTFM_API_KEY

client = LastFMClient(api_key=LASTFM_API_KEY)

data = client.get_recent_tracks_page(user="fredzell", page=2)

print(data)
from src.clients.lastfm_client import LastFMClient
from src.config import LASTFM_API_KEY

from datetime import datetime
import pandas as pd
import time
import os


USERNAME = "fredzell"


# ---------- helpers ----------

def to_unix(dt):
    return int(dt.timestamp())


def parse_track(t):
    return {
        "artist": t.get("artist", {}).get("#text"),
        "track": t.get("name"),
        "timestamp": t.get("date", {}).get("uts"),
    }


# ---------- core logic ----------

def fetch_year(client, username, year):
    from_ts = to_unix(datetime(year, 1, 1))
    to_ts = to_unix(datetime(year, 12, 31))

    page = 1
    all_tracks = []

    while True:
        print(f"[{year}] page {page}")

        data = client.get_recent_tracks_page(
            user=username,
            page=page,
            limit=200,
            from_ts=from_ts,
            to_ts=to_ts,
        )

        tracks = data.get("recenttracks", {}).get("track", [])

        # importans as sometimes it is a dict instead of a list
        if isinstance(tracks, dict):
            tracks = [tracks]

        if not tracks:
            break

        parsed = [parse_track(t) for t in tracks]
        all_tracks.extend(parsed)

        page += 1
        time.sleep(0.2)

    return all_tracks


# ---------- main ----------

def main():
    client = LastFMClient(api_key=LASTFM_API_KEY)

    all_data = []

    for year in range(2007, 2027):
        year_tracks = fetch_year(client, USERNAME, year)

        print(f"{year}: {len(year_tracks)} tracks")

        # checkpoint per year
        os.makedirs("data/raw/lastfm", exist_ok=True)

        pd.DataFrame(year_tracks).to_parquet(
            f"data/raw/lastfm/scrobbles_{year}.parquet",
            index=False
        )

        all_data.extend(year_tracks)

    print(f"\nTOTAL tracks: {len(all_data)}")

    # save all
    df = pd.DataFrame(all_data)

    df.to_parquet("data/raw/lastfm/scrobbles_raw.parquet", index=False)


if __name__ == "__main__":
    main()
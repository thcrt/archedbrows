from datetime import datetime

import arrow

from archedbrows.downloader.common import InfoDict
from archedbrows.models import Post


def parse_post(url: str, meta: InfoDict) -> Post:
    title = meta.get("title", "untitled")
    author = meta.get("uploader_id")
    time = datetime.fromtimestamp(meta["timestamp"]) if "timestamp" in meta else None
    source = f"{meta.get('extractor')} {meta.get('_type')}"
    text = meta.get("description")

    # Override some metadata keys for specific platforms with known variations from the standard
    # pattern
    match meta["extractor"]:
        case "archive.org":
            author = meta.get("creator")
        case "Erocast":
            author = meta.get("uploader")
            time = datetime.fromtimestamp(meta["release_timestamp"])
        case "Motherless":
            time = arrow.get(meta["upload_date"]).datetime
        case "RedGifs":
            author = meta.get("uploader")
        case "soundcloud":
            author = meta.get("uploader")
        case "Bandcamp:album":
            time = datetime.fromtimestamp(meta["entries"][0]["release_timestamp"])
        case _:
            pass

    return Post(
        title=title,
        author=author,
        time_created=time,
        source=source,
        source_url=url,
        text=text,
    )

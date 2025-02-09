import mimetypes
from contextlib import redirect_stdout
from datetime import datetime
from typing import Any, override

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from ...database import Media, Post
from ..common import Downloader, UnsupportedURLError
from ..util import PersistentBytes

YTDLP_OPTIONS = {"outtmpl": "-", "logtostderr": True}


def parse_post(url: str, meta: dict[str, Any]) -> Post:
    return Post(
        title=meta["title"],
        author=meta["uploader"],
        time=datetime.fromtimestamp(meta["timestamp"]),
        source=f"{meta['extractor_key']} {meta['_type']}",
        source_url=url,
        text=meta["description"],
    )


class YTDLPDownloader(Downloader):
    @override
    def run(self) -> Post:
        buffer = PersistentBytes()
        with redirect_stdout(buffer), YoutubeDL(YTDLP_OPTIONS) as ydl:  # type: ignore[type-var]
            try:
                meta = ydl.sanitize_info(ydl.extract_info(self.url))
            except DownloadError as e:
                if "Unsupported URL" in e.msg:
                    raise UnsupportedURLError(self.url) from e
                else:
                    raise

        post = parse_post(self.url, meta)
        filename = f"{meta['id']}.{meta['ext']}"
        post.media.append(
            Media(buffer.getvalue(), filename=filename, mime_type=mimetypes.guess_type(filename)[0])
        )

        buffer.real_close()
        return post

import mimetypes
from contextlib import redirect_stdout
from copy import deepcopy
from typing import Any, cast, override

from yt_dlp import YoutubeDL
from yt_dlp.networking.exceptions import HTTPError
from yt_dlp.networking.impersonate import ImpersonateTarget
from yt_dlp.utils import DownloadError

from ...database import Media, Post
from ..common import Downloader, UnsupportedURLError
from ._memory import Meta, MultipleFileBuffer
from .metadata import parse_post

YTDLP_OPTIONS = {
    "outtmpl": "-",
    "logtostderr": True,
    "progress_hooks": [],
}
YTDLP_IMPERSONATE_OPTIONS = {
    "impersonate": ImpersonateTarget(client="chrome", os="windows", os_version="10")
}


class YTDLPDownloader(Downloader):
    options: dict[str, Any]

    def __init__(self, url: str):
        super().__init__(url)
        self.options = YTDLP_OPTIONS

    def _run(self, options: Meta) -> Meta:
        with YoutubeDL(options) as ydl:
            return cast(Meta, ydl.extract_info(self.url))

    @override
    def run(self) -> Post:
        with MultipleFileBuffer() as buffer:
            options = deepcopy(self.options)
            options["progress_hooks"].append(buffer.callback)

            with redirect_stdout(buffer):  # type: ignore[type-var]
                try:
                    meta = self._run(options)
                except DownloadError as e:
                    if isinstance(e.exc_info[1], HTTPError) and e.exc_info[1].status == 403:
                        # Try again, but pretend to be a human
                        meta = self._run(options | YTDLP_IMPERSONATE_OPTIONS)
                    elif (
                        "Unsupported URL" in e.msg
                        or "The given url does not contain a video" in e.msg
                    ):
                        raise UnsupportedURLError(self.url) from e
                    else:
                        raise

            post = parse_post(self.url, meta)
            for file_meta, file in buffer.files:
                filename = f"{file_meta['id']}.{file_meta['ext']}"
                post.media.append(
                    Media(file, filename=filename, mime_type=mimetypes.guess_type(filename)[0])
                )

            return post

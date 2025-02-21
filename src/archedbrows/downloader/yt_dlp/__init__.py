import mimetypes
from contextlib import redirect_stdout
from typing import TYPE_CHECKING, cast, override

from yt_dlp import YoutubeDL
from yt_dlp.networking.exceptions import HTTPError
from yt_dlp.networking.impersonate import ImpersonateTarget
from yt_dlp.utils import DownloadError

from archedbrows.downloader.common import (
    Downloader,
    InfoDict,
    MultipleFileBuffer,
    UnsupportedURLError,
)
from archedbrows.models import Media, Post

from .metadata import parse_post

if TYPE_CHECKING:
    from yt_dlp import YDLOpts

IMPERSONATE_OPTIONS: YDLOpts = {
    "impersonate": ImpersonateTarget(client="chrome", os="windows", os_version="10")
}


class YTDLPDownloader(Downloader):
    options: YDLOpts

    def __init__(self, url: str) -> None:
        super().__init__(url)
        self.options: YDLOpts = {
            "outtmpl": "-",
            "logtostderr": True,
            "progress_hooks": [],
        }

    def _run(self) -> InfoDict:
        with YoutubeDL(self.options) as ydl:
            return cast(InfoDict, ydl.extract_info(self.url))

    @override
    def run(self) -> Post:
        with MultipleFileBuffer() as buffer:
            assert "progress_hooks" in self.options
            self.options["progress_hooks"].append(buffer.callback)

            with redirect_stdout(buffer):  # type: ignore[type-var]
                try:
                    meta = self._run()
                except DownloadError as e:
                    assert isinstance(e, DownloadError)
                    if (
                        e.exc_info
                        and isinstance(e.exc_info[1], HTTPError)
                        and e.exc_info[1].status == 403
                    ):
                        # Try again, but pretend to be a human
                        self.options.update(IMPERSONATE_OPTIONS)
                        meta = self._run()
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
                    Media(file, filename=filename, mime_type=mimetypes.guess_file_type(filename)[0])
                )

            return post

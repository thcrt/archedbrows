import mimetypes
from typing import override

import gallery_dl.config
from gallery_dl.exception import NoExtractorError

from ...database import Media, Post
from ..common import Downloader, UnsupportedURLError
from ._memory import InMemoryDownloadJob
from .metadata import parse_post

gallery_dl.config.load()
gallery_dl.config.set(("extractor",), "metadata", True)
gallery_dl.config.set(("extractor",), "browser", "firefox")


class GalleryDLDownloader(Downloader):
    def __init__(self, url: str):
        super().__init__(url)
        try:
            self.job = InMemoryDownloadJob(url)
        except NoExtractorError as e:
            raise UnsupportedURLError(url) from e

    @override
    def run(self) -> Post:
        self.job.run()
        post = parse_post(self.url, self.job.metadata)
        for filename, file in self.job.files.items():
            post.media.append(
                Media(file, filename=filename, mime_type=mimetypes.guess_type(filename)[0])
            )
        return post

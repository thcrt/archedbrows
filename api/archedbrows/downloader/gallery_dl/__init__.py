import mimetypes
from typing import override

from gallery_dl.exception import NoExtractorError  # type: ignore
from gallery_dl_bytes import DownloadJob, set_config

from archedbrows.downloader.common import Downloader, UnsupportedURLError
from archedbrows.models import Media, Post

from .metadata import parse_post

set_config(("extractor",), "metadata", True)
set_config(("extractor",), "browser", "firefox")


class GalleryDLDownloader(Downloader):
    def __init__(self, url: str) -> None:
        super().__init__(url)
        try:
            self.job = DownloadJob(url)
        except NoExtractorError as e:
            raise UnsupportedURLError(url) from e

    @override
    def run(self) -> Post:
        self.job.run()
        files = self.job.files
        post = parse_post(self.url, self.job.metadata)
        for file in files:
            post.media.append(
                Media(
                    file.data,
                    filename=str(file.name),
                    mime_type=mimetypes.guess_file_type(str(file.name))[0],
                )
            )
        return post

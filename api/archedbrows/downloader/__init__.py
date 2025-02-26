from archedbrows.models import Post

from .common import UnsupportedURLError
from .gallery_dl import GalleryDLDownloader
from .yt_dlp import YTDLPDownloader

DOWNLOADERS = [
    GalleryDLDownloader,
    YTDLPDownloader,
]


def download_post(url: str) -> Post:
    for downloader in DOWNLOADERS:
        try:
            return downloader(url).run()
        except UnsupportedURLError:
            pass
    raise UnsupportedURLError(url)

import mimetypes

import gallery_dl.config  # type: ignore

from ...database import Media, Post
from ._memory import InMemoryDownloadJob
from .metadata import parse_post

gallery_dl.config.load()
gallery_dl.config.set(("extractor",), "metadata", True)
gallery_dl.config.set(("extractor",), "browser", "firefox")


def download_post(url: str) -> Post:
    job = InMemoryDownloadJob(url)
    job.run()

    post = parse_post(url, job.metadata)
    for filename, file in job.files.items():
        post.media.append(
            Media(file, filename=filename, mime_type=mimetypes.guess_type(filename)[0])
        )

    return post

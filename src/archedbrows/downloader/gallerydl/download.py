import gallery_dl.config  # type: ignore
import gallery_dl.extractor.imgur  # type: ignore

from ...database import Media, Post
from ._memory import InMemoryDownloadJob
from .metadata import parse_post

gallery_dl.config.load()
gallery_dl.config.set(("extractor",), "metadata", True)
gallery_dl.config.set(("extractor",), "browser", "firefox")
gallery_dl.config.set(("output",), "log", {"level": "debug"})


def download_post(url: str) -> Post:
    job = InMemoryDownloadJob(url)
    job.run()

    if isinstance(job.extractor, gallery_dl.extractor.imgur.ImgurGalleryExtractor):
        extractor = list(job.extractor.items())[0][2]["_extractor"](job.extractor.match)
        extractor.initialize()
    else:
        extractor = job.extractor

    metadata = next(extractor.items())[1]
    metadata.update(
        {
            "category": extractor.category,
            "subcategory": extractor.subcategory,
            "basecategory": extractor.basecategory,
        }
    )

    post = parse_post(url, metadata)

    for file in job.pathfmt.files.values():
        post.media.append(Media(file))

    return post

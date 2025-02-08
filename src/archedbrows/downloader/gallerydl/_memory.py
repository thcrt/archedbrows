from io import BytesIO
from typing import Any, cast

from gallery_dl.extractor.common import Extractor  # type: ignore
from gallery_dl.job import DownloadJob, Job  # type: ignore
from gallery_dl.path import PathFormat  # type: ignore


class PersistentBytes(BytesIO):
    def close(self) -> None:
        # This prevents the default behaviour of closing the buffer when exiting a `with` block, as
        # well as the standard API of calling `.close()` manually. There's a good reason for it,
        # though! `gallery_dl` internally will close the IO object that it gets from `pathfmt` in a
        # few places, which make sense for writing to a file. But we want to only store the download
        # in memory, not to a file, so we need to make sure the IO object stays open until we're
        # done with it.
        pass

    def real_close(self) -> None:
        return super().close()


# mypy: allow_subclassing_any
class InMemoryFormat(PathFormat):
    files: dict[str, bytes]

    def __init__(self, extractor: Extractor):
        super().__init__(extractor)
        self.files = {}

    def open(self, mode: str) -> PersistentBytes:
        self._data = data = PersistentBytes()
        return data

    def finalize(self) -> None:
        self.files[self.filename] = self._data.getvalue()
        self._data.real_close()


class InMemoryDownloadJob(DownloadJob):
    def __init__(self, url: str, parent: Job | None = None):
        super().__init__(url, parent)
        self.initialize()
        self.pathfmt = InMemoryFormat(self.extractor)

    @property
    def metadata(self) -> dict[str, Any]:
        return cast(dict[str, Any], self.pathfmt.kwdict)

    @property
    def files(self) -> dict[str, bytes]:
        return self.pathfmt.files

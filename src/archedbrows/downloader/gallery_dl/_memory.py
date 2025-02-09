from typing import Any, Self

import gallery_dl.extractor
from gallery_dl.extractor.common import Extractor
from gallery_dl.job import DownloadJob, Job
from gallery_dl.path import PathFormat
from gallery_dl.text import nameext_from_url

from ..util import PersistentBytes

type KWDict = dict[str, Any]


# mypy: allow_subclassing_any
class InMemoryFormat(PathFormat):
    files: dict[str, bytes]
    kwdict: KWDict

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
    extractor: Extractor
    _skipcnt: int
    children: list[Self]

    def __init__(self, extractor: str | Extractor, parent: Job | None = None):
        super().__init__(extractor, parent)
        self.children = []
        self.initialize()
        self.pathfmt = InMemoryFormat(self.extractor)

    @property
    def metadata(self) -> KWDict:
        metadata = self.pathfmt.kwdict
        for child in self.children:
            metadata = metadata | child.metadata
        return metadata

    @property
    def files(self) -> dict[str, bytes]:
        files = self.pathfmt.files
        for child in self.children:
            files = files | child.files
        return files

    def handle_queue(self, url: str, kwdict: KWDict) -> None:
        if url in self.visited:
            return
        self.visited.add(url)

        extractor: Extractor | None
        cls: Extractor | None
        if cls := kwdict.get("_extractor"):
            extractor = cls.from_url(url)
        else:
            extractor = gallery_dl.extractor.find(url)
            if extractor:
                if self._extractor_filter is None:
                    self._extractor_filter: Any = self._build_extractor_filter()
                if not self._extractor_filter(extractor):
                    extractor = None

        if not extractor:
            self._write_unsupported(url)
            return

        child_job = self.__class__(extractor, self)

        parent_metadata = self.extractor.config2("parent-metadata", "metadata-parent")
        if parent_metadata:
            if isinstance(parent_metadata, str):
                data = self.kwdict.copy()
                if kwdict:
                    data.update(kwdict)
                child_job.kwdict[parent_metadata] = data
            else:
                if self.kwdict:
                    child_job.kwdict.update(self.kwdict)
                if kwdict:
                    child_job.kwdict.update(kwdict)

        while True:
            try:
                if self.extractor.config("parent-skip"):
                    child_job._skipcnt = self._skipcnt

                status = child_job.run()

                if self.extractor.config("parent-skip"):
                    self._skipcnt = child_job._skipcnt

                if status:
                    self.status |= status
                    if status & 95 and "_fallback" in kwdict and self.fallback:
                        fallback = kwdict["_fallback"] = iter(kwdict["_fallback"])
                        try:
                            url = next(fallback)
                        except StopIteration:
                            pass
                        else:
                            nameext_from_url(url, kwdict)
                            self.handle_url(url, kwdict)

                break

            except gallery_dl.exception.RestartExtraction:
                pass

        self.children.append(child_job)

import textwrap
from abc import ABC, abstractmethod
from io import BytesIO
from types import TracebackType
from typing import TYPE_CHECKING, Any, Self

from markupsafe import Markup

from ..database import Post

if TYPE_CHECKING:
    from _typeshed import ReadableBuffer

type InfoDict = dict[str, Any]


class Downloader(ABC):
    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def run(self) -> Post: ...


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


class MultipleFileBuffer:
    files: list[tuple[InfoDict, bytes]]
    _current: BytesIO

    def __init__(self) -> None:
        self.files = []
        self._current = BytesIO()

    def callback(self, info: InfoDict) -> None:
        if info["status"] in ("error", "finished"):
            self.files.append((info["info_dict"], self._current.getvalue()))
            self._current = BytesIO()

    def write(self, buffer: "ReadableBuffer") -> int:
        return self._current.write(buffer)

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self._current.close()


class UnsupportedURLError(Exception):
    pass


def content_to_title(content: str) -> str:
    return textwrap.shorten(Markup(content).striptags(), width=75, placeholder="...")

from io import BytesIO
from types import TracebackType
from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:
    from _typeshed import ReadableBuffer

type Meta = dict[str, Any]


class MultipleFileBuffer:
    files: list[tuple[Meta, bytes]]
    _current: BytesIO

    def __init__(self) -> None:
        self.files = []
        self._current = BytesIO()

    def callback(self, info: dict[str, Any]) -> None:
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

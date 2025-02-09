import textwrap
from io import BytesIO

from markupsafe import Markup


def content_to_title(content: str) -> str:
    return textwrap.shorten(Markup(content).striptags(), width=75, placeholder="...")


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

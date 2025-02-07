import textwrap

from markupsafe import Markup


def content_to_title(content: str) -> str:
    return textwrap.shorten(Markup(content).striptags(), width=75, placeholder="...")

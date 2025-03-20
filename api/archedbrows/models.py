from dataclasses import InitVar
from datetime import datetime
from enum import StrEnum, auto
from io import BytesIO
from mimetypes import guess_extension
from pathlib import Path, PurePath
from typing import TYPE_CHECKING, Any, cast
from uuid import uuid4

import av
import av.container
import humanize
from flask import current_app as app
from PIL import Image
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from . import db

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model
else:
    Model = db.Model


THUMBNAIL_MAX_DIMENSIONS = (1024, 1024)
THUMBNAIL_TYPE = "JPEG"

MEDIA_DIR = Path(app.instance_path) / "media"
THUMBS_DIR = Path(app.instance_path) / "thumbs"

MEDIA_DIR.mkdir(exist_ok=True)
THUMBS_DIR.mkdir(exist_ok=True)


class Media(MappedAsDataclass, Model):
    class MediaType(StrEnum):
        AUDIO = auto()
        IMAGE = auto()
        VIDEO = auto()

    __tablename__ = "images"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    init_data: InitVar[bytes]
    file_id: Mapped[str] = mapped_column(init=False)
    source_filename: Mapped[str | None] = mapped_column(default=None)
    mime_type: Mapped[str | None] = mapped_column(default=None)
    post_id: Mapped[int | None] = mapped_column(ForeignKey("posts.id"), default=None)
    post: Mapped["Post | None"] = relationship(back_populates="media", default=None)

    def __post_init__(self, init_data: bytes) -> None:
        # We need to use UUIDs for the filenames, because the actual database ID isn't avaialable to
        # us yet in __post_init__ :(
        self.file_id = uuid4().hex
        self.data = init_data
        self.generate_thumb()

    def generate_thumb(self) -> None:
        if self.type == self.MediaType.VIDEO:
            with (
                BytesIO(self.data) as data,
                av.open(data) as container,
            ):
                container = cast(av.container.InputContainer, container)
                video = container.streams.video[0]
                video.codec_context.skip_frame = "NONKEY"

                frame = next(container.decode(video)).to_image()
                frame.thumbnail(THUMBNAIL_MAX_DIMENSIONS)

                frame.save(THUMBS_DIR / f"{self.file_id}.jpg")
        elif self.type == self.MediaType.IMAGE:
            with BytesIO(self.data) as data:
                im = Image.open(data)
                im.thumbnail(THUMBNAIL_MAX_DIMENSIONS)
                im.save(THUMBS_DIR / f"{self.file_id}.jpg")

    @property
    def thumb(self) -> bytes | None:
        def _impl() -> bytes | None:
            try:
                return (THUMBS_DIR / f"{self.file_id}.jpg").read_bytes()
            except FileNotFoundError:
                return None

        thumb = _impl()
        if thumb:
            return thumb
        self.generate_thumb()
        return _impl()

    @property
    def extension(self) -> str:
        if self.source_filename:
            path_suffix = PurePath(self.source_filename).suffix
            guessed = guess_extension(self.source_filename)
            if path_suffix:
                return path_suffix
            if guessed:
                return guessed
        return ""

    @property
    def filename(self) -> str:
        return f"{self.file_id}{self.extension}"

    @property
    def data(self) -> bytes:
        return (MEDIA_DIR / self.filename).read_bytes()

    @data.setter
    def data(self, value: bytes) -> None:
        with (MEDIA_DIR / self.filename).open("wb+") as f:
            _ = f.write(value)

    @hybrid_property
    def type(self) -> MediaType | None:
        if self.mime_type is None:
            return None

        main_type = self.mime_type.split("/", 1)[0].lower()
        if main_type in self.MediaType:
            return self.MediaType(main_type)
        return None

    def to_dict(self) -> dict[str, int | str | None]:
        return {
            "id": self.id,
            "filename": self.source_filename,
            "type": self.type,
        }


class Post(MappedAsDataclass, Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    source: Mapped[str]
    source_url: Mapped[str]

    title: Mapped[str]
    author: Mapped[str | None] = mapped_column(default=None)
    time_created: Mapped[datetime | None] = mapped_column(default=None)
    time_added: Mapped[datetime] = mapped_column(default_factory=datetime.now)

    text: Mapped[str | None] = mapped_column(default=None)
    media: Mapped[list[Media]] = relationship(
        back_populates="post", cascade="all, delete-orphan", default_factory=list
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "source": self.source,
            "source_url": self.source_url,
            "title": self.title,
            "author": self.author,
            "time_created": self.time_created.isoformat() if self.time_created else None,
            "time_added": self.time_added.isoformat(),
            "text": self.text,
            "media": [media.to_dict() for media in self.media],
        }

    @hybrid_property
    def time_ago_created(self) -> str | None:
        return (
            humanize.naturaltime(datetime.now() - self.time_created) if self.time_created else None
        )

    @hybrid_property
    def time_ago_added(self) -> str | None:
        return humanize.naturaltime(datetime.now() - self.time_added) if self.time_added else None

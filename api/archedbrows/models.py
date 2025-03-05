from datetime import datetime
from enum import StrEnum, auto
from io import BytesIO
from typing import TYPE_CHECKING, Any, cast

import av
import av.container
import humanize
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


class Media(MappedAsDataclass, Model):
    class MediaType(StrEnum):
        AUDIO = auto()
        IMAGE = auto()
        VIDEO = auto()

    __tablename__ = "images"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    data: Mapped[bytes]
    thumb: Mapped[bytes | None] = mapped_column(default=None)
    filename: Mapped[str | None] = mapped_column(default=None)
    mime_type: Mapped[str | None] = mapped_column(default=None)
    post_id: Mapped[int | None] = mapped_column(ForeignKey("posts.id"), default=None)
    post: Mapped["Post | None"] = relationship(back_populates="media", default=None)

    def __post_init__(self) -> None:
        self.generate_thumb()

    def generate_thumb(self) -> None:
        if self.type == self.MediaType.VIDEO:
            with BytesIO(self.data) as data, av.open(data) as container, BytesIO() as thumb:
                container = cast(av.container.InputContainer, container)
                video = container.streams.video[0]
                video.codec_context.skip_frame = "NONKEY"

                frame = next(container.decode(video)).to_image()
                frame.thumbnail(THUMBNAIL_MAX_DIMENSIONS)
                frame.save(thumb, format=THUMBNAIL_TYPE)
                self.thumb = thumb.getvalue()

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
            "filename": self.filename,
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

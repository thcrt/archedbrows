from datetime import datetime
from typing import TYPE_CHECKING

import humanize
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, relationship


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model
else:
    Model = db.Model


class Media(MappedAsDataclass, Model):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    data: Mapped[bytes]
    mime_type: Mapped[str] = mapped_column(default_factory=str)
    post_id: Mapped[int | None] = mapped_column(ForeignKey("posts.id"), default=None)
    post: Mapped["Post | None"] = relationship(back_populates="media", default=None)


class Post(MappedAsDataclass, Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    time: Mapped[datetime]
    source: Mapped[str]
    source_url: Mapped[str]

    text: Mapped[str | None] = mapped_column(default=None)
    media: Mapped[list[Media]] = relationship(back_populates="post", default_factory=list)

    @hybrid_property
    def time_ago(self) -> str:
        return humanize.naturaltime(datetime.now() - self.time)

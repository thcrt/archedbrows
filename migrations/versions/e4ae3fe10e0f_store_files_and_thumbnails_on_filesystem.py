"""Store files and thumbnails on filesystem.

Revision ID: e4ae3fe10e0f
Revises: 32ec4859da01
Create Date: 2025-03-17 00:52:13.109305

"""

from collections.abc import Sequence
from datetime import datetime
from mimetypes import guess_extension
from pathlib import Path, PurePath

import sqlalchemy as sa
from alembic import op
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, relationship
from sqlalchemy.orm.session import Session

# revision identifiers, used by Alembic.
revision: str = "e4ae3fe10e0f"
down_revision: str | None = "32ec4859da01"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


# Define static versions of the models
class Base(DeclarativeBase):
    pass


class MediaPreUpgrade(MappedAsDataclass, Base):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    data: Mapped[bytes]
    thumb: Mapped[bytes | None] = mapped_column(default=None)
    filename: Mapped[str | None] = mapped_column(default=None)
    mime_type: Mapped[str | None] = mapped_column(default=None)
    post_id: Mapped[int | None] = mapped_column(sa.ForeignKey("posts.id"), default=None)
    post: Mapped["Post"] = relationship(back_populates="media", default=None)

    @property
    def extension(self) -> str:
        if self.filename:
            path_suffix = PurePath(self.filename).suffix
            guessed = guess_extension(self.filename)
            if path_suffix:
                return path_suffix
            if guessed:
                return guessed
        return ""

    @property
    def storage_filename(self) -> str:
        return f"{self.id}{self.extension}"


class Post(MappedAsDataclass, Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    source: Mapped[str]
    source_url: Mapped[str]

    title: Mapped[str]
    author: Mapped[str | None] = mapped_column(default=None)
    time_created: Mapped[datetime | None] = mapped_column(default=None)
    time_added: Mapped[datetime] = mapped_column(default_factory=datetime.now)

    text: Mapped[str | None] = mapped_column(default=None)
    media: Mapped[list[MediaPreUpgrade]] = relationship(
        back_populates="post", cascade="all, delete-orphan", default_factory=list
    )

    @hybrid_property
    def time_ago_created(self) -> str | None: ...

    @hybrid_property
    def time_ago_added(self) -> str | None: ...


def upgrade() -> None:
    for old_media_obj in Session(bind=op.get_bind()).query(MediaPreUpgrade).all():
        _ = Path(f"media/{old_media_obj.storage_filename}").write_bytes(old_media_obj.data)
        if old_media_obj.thumb:
            _ = Path(f"thumbs/{old_media_obj.id}.jpg").write_bytes(old_media_obj.thumb)

    with op.batch_alter_table("images", schema=None) as batch_op:
        batch_op.alter_column("filename", new_column_name="source_filename")
        batch_op.drop_column("data")
        batch_op.drop_column("thumb")

"""Use UUID for saved media files.

Revision ID: b8768c58d2cb
Revises: e4ae3fe10e0f
Create Date: 2025-03-20 01:34:01.431080

"""

import contextlib
from collections.abc import Sequence
from dataclasses import InitVar
from datetime import datetime
from mimetypes import guess_extension
from pathlib import Path, PurePath
from uuid import uuid4

import sqlalchemy as sa
from alembic import op
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    Session,
    mapped_column,
)

# revision identifiers, used by Alembic.
revision: str = "b8768c58d2cb"
down_revision: str | None = "e4ae3fe10e0f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


# Define static versions of the models
class Base(DeclarativeBase):
    pass


class MediaPreUpgrade(MappedAsDataclass, Base):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    init_data: InitVar[bytes]
    source_filename: Mapped[str | None] = mapped_column(default=None)
    mime_type: Mapped[str | None] = mapped_column(default=None)
    post_id: Mapped[int | None] = mapped_column(sa.ForeignKey("posts.id"), default=None)

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


class MediaPostUpgrade(MappedAsDataclass, Base):
    __tablename__ = "images"
    __table_args__ = {"extend_existing": True}
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    init_data: InitVar[bytes]
    file_id: Mapped[str] = mapped_column(init=False)
    source_filename: Mapped[str | None] = mapped_column(default=None)
    mime_type: Mapped[str | None] = mapped_column(default=None)
    post_id: Mapped[int | None] = mapped_column(sa.ForeignKey("posts.id"), default=None)

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



def upgrade() -> None:
    new_uuids: dict[int, str] = {}
    session = Session(bind=op.get_bind())

    for media_obj in session.query(MediaPreUpgrade).all():
        new_uuid = uuid4().hex
        new_uuids[media_obj.id] = new_uuid
        try:
            _ = Path(f"media/{media_obj.id}{media_obj.extension}").rename(
                f"media/{new_uuid}{media_obj.extension}"
            )
        except FileNotFoundError:
            print(f"WARNING: No file media/{media_obj.id}{media_obj.extension}")
        with contextlib.suppress(FileNotFoundError):
            _ = Path(f"thumbs/{media_obj.id}.jpg").rename(f"thumbs/{new_uuid}.jpg")

    with op.batch_alter_table("images", schema=None) as batch_op:
        batch_op.add_column(sa.Column("file_id", sa.String(), nullable=True))

    for media_obj in session.query(MediaPostUpgrade).all():
        media_obj.file_id = new_uuids[media_obj.id]
        session.commit()

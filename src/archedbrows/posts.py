from dataclasses import dataclass, field
from datetime import datetime
from typing import Self

import humanize


@dataclass
class Post:
    title: str
    user: str
    time: datetime
    source: str
    images: list[str] = field(default_factory=list)
    text: str | None = None

    @property
    def time_ago(self) -> str:
        return humanize.naturaltime(datetime.now() - self.time)


class PostManager:
    posts: list[Post]

    def __init__(self) -> None:
        self.posts = []

    @classmethod
    def with_dummy_data(cls) -> Self:
        pm = cls()

        pm.posts = [
            Post(
                title="Foo foofoo foofoofoofoo foo",
                user="alice",
                time=datetime.fromisoformat("2020-01-01T00:00:00"),
                source="reddit",
                images=["image.jpg"],
            ),
            Post(
                title="Bar barbar barbarbarbar bar",
                user="bob",
                time=datetime.fromisoformat("2020-01-01T00:00:00"),
                source="reddit",
                images=["image.jpg"],
            ),
            Post(
                title="Baz bazbaz bazbazbazbaz baz",
                user="charlie",
                time=datetime.fromisoformat("2020-01-01T00:00:00"),
                source="reddit",
                images=["image.jpg"],
            ),
        ]

        return pm

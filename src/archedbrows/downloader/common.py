from abc import ABC, abstractmethod

from archedbrows.database import Post


class Downloader(ABC):
    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def run(self) -> Post: ...


class UnsupportedURLError(Exception):
    pass

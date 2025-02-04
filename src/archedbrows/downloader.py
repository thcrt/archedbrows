import json
import subprocess
from datetime import datetime
from pathlib import Path

from .database import Media, Post


class Downloader:
    download_dir: Path

    def __init__(self, download_dir: Path = Path("/tmp/archedbrows")) -> None:
        download_dir.mkdir(exist_ok=True)
        self.download_dir = download_dir

    def download_post(self, url: str) -> Post:
        download_process = subprocess.run(
            ["gallery-dl", "--write-info-json", "-D", str(self.download_dir), url],
            capture_output=True,
            text=True,
        )

        info_path = self.download_dir / "info.json"
        media_paths = [
            Path(media_path.strip(" #"))
            for media_path in download_process.stdout.split("\n")
            if media_path != ""
        ]


        info = json.loads(info_path.read_text())

        post = Post(
            title=info["title"],
            author=info["author"],
            time=datetime.fromisoformat(info["date"]),
            source=f"{info['category']} {info['subcategory']}",
            source_url=url,
            text=info["selftext_html"],
        )

        for media_path in media_paths:
            post.media.append(Media(media_path.read_bytes()))

        return post

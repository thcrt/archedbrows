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
        media_path = None
        if download_process.stdout.strip("\n# "):
            media_path = Path(download_process.stdout.strip("\n# "))


        info = json.loads(info_path.read_text())

        post = Post(
            title=info["title"],
            author=info["author"],
            time=datetime.fromisoformat(info["date"]),
            source=f"{info['category']} {info['subcategory']}",
            source_url=url,
            text=info["selftext_html"],
        )

        if media_path:
            post.media.append(Media(media_path.read_bytes()))

        return post

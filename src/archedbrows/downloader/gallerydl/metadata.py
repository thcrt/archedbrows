from datetime import datetime
from typing import Any

import arrow

from ...database import Post
from ..util import content_to_title


def parse_post(url: str, info: dict[str, Any]) -> Post:
    # Handle federated software with multiple instances, marked by a 'foo:' prefix
    if url.startswith("mastodon:") or info["category"] == "mastodon.social":
        username = info["account"]["username"]
        instance = info["instance_remote"] if info["instance_remote"] else info["instance"]
        return Post(
            title=content_to_title(info["content"]),
            author=f"@{username}@{instance}",
            time=info["created_at"],
            source=f"{info['category']} {info['subcategory']}",
            source_url=url.removeprefix("mastodon:"),
            text=info["content"],
        )

    match (info["category"], info["subcategory"]):
        case ("35photo", "image"):
            return Post(
                title=info["title"],
                author=info["user"],
                time=arrow.utcnow().dehumanize(info["date"]).datetime,
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["description"],
            )
        case ("500px", "image"):
            return Post(
                title=info["name"],
                author=info["user"]["username"],
                time=datetime.fromisoformat(info["created_at"]),
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["description"],
            )
        case ("4chan", _):
            # TODO: This needs work on handling the thread vs individual posts on it
            raise NotImplementedError
        case ("ao3", "work"):
            # TODO: gallery-dl saves works as PDFs and not text
            raise NotImplementedError
        case ("behance", "gallery"):
            return Post(
                title=info["name"],
                author=info["creator"]["displayName"],
                time=info["date"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["description"],
            )
        case ("bluesky", "post"):
            return Post(
                title=content_to_title(info["text"]),
                author=info["author"]["handle"],
                time=datetime.fromisoformat(info["createdAt"]),
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["text"],
            )
        case ("bunkr", "media"):
            # TODO: This doesn't give us a decent title
            return Post(
                title="untitled",
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
            )
        case ("bunkr", "album"):
            return Post(
                title=info["album_name"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
            )
        case ("catbox", "file"):
            return Post(
                title=info["filename"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
            )
        case ("catbox", "album"):
            return Post(
                title=info["album_name"],
                time=info["date"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["description"],
            )
        case ("coomerparty", "onlyfans"):
            # TODO: This also accepts entire profiles (not just posts), which causes jank
            return Post(
                title=info["title"],
                author=info["user"],
                time=datetime.fromisoformat(info["published"]),
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["content"],
            )
        case ("coomerparty", "fansly"):
            # TODO: This also accepts entire profiles (not just posts), which causes jank
            return Post(
                title=info["title"],
                author=info["username"],
                time=datetime.fromisoformat(info["published"]),
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["content"],
            )
        case ("deviantart", "deviation"):
            return Post(
                title=info["title"],
                author=info["username"],
                time=info["date"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["description"],
            )
        case ("erome", "album"):
            return Post(
                title=info["title"],
                author=info["user"],
                time=info["date"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
            )
        case ("fapello", "post"):
            return Post(
                title=f"{info['type'].capitalize()} #{info['id']}",
                author=info["model"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
            )
        case ("flickr", "image"):
            return Post(
                title=info["title"],
                author=info["user"]["username"],
                time=info["date"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["description"],
            )
        case ("flickr", "gallery"):
            return Post(
                title=info["gallery"]["title"],
                author=info["gallery"]["username"],
                time=datetime.fromtimestamp(int(info["gallery"]["date_create"])),
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["gallery"]["description"],
            )
        case ("furaffinity", "post"):
            return Post(
                title=info["title"],
                author=info["user"],
                time=datetime.fromisoformat(info["date"]),
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["description"],
            )
        case ("gelbooru" | "paheal" | "rule34us" | "rule34xyz", _):
            # TODO: This site doesn't have titles, should look into grabbing from original
            # source instead
            raise NotImplementedError
        case ("gofile", "folder"):
            # TODO: It seems to be possible to share individual files, but this requires a paid
            # account to test
            return Post(
                title=info["name"],
                time=datetime.fromtimestamp(int(info["createTime"])),
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
            )
        case ("imagebam", "gallery"):
            return Post(
                title=info["title"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
            )
        case ("imagebam", "image"):
            return Post(
                title=info["filename"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
            )
        case ("imagechest", "gallery"):
            return Post(
                title=info["title"],
                author=info["user"]["username"],
                time=arrow.utcnow().dehumanize(info["created"]).datetime,
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
            )
        case ("imgbb", "album"):
            return Post(
                title=info["album_name"],
                author=info["user"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
            )
        case ("imgbb", "image"):
            return Post(
                title=info["title"],
                author=info["user"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
            )
        case ("imgbox", _):
            # TODO: Current implementation gives us literally 0 metadata
            raise NotImplementedError
        case ("imgur", "image"):
            # Note that most posts are actually albums - if you click a post on the front page,
            # it'll take you to the album. It's possible to get the image alone, which we handle
            # here, but it's missing some metadata. Most of the time, the user will probably use
            # imgur/album below.
            return Post(
                title=info["title"],
                time=datetime.fromisoformat(info["created_at"]),
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["description"],
            )
        case ("imgur", "album"):
            # TODO: Descriptions are on a per-image basis, and this only captures the first
            # image's description
            return Post(
                title=info["album"]["title"],
                author=info["album"]["account"]["username"],
                time=datetime.fromisoformat(info["album"]["created_at"]),
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["description"],
            )
        case ("instagram", _):
            # TODO: We seem to get blocked when downloading an individual post, and downloading
            # a whole profile seems fine but gets rate-limited super fast. Downloading a whole
            # profile seems like it would be better to create multiple posts instead of just
            # one.
            raise NotImplementedError
        case ("issuu", "publication"):
            # TODO: This gets us JPGs, we should probably try to get PDFs
            return Post(
                title=info["document"]["title"],
                author=info["document"]["username"],
                time=datetime.fromisoformat(info["document"]["originalPublishDateInISOString"]),
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["document"]["description"],
            )
        case ("itaku", "image"):
            return Post(
                title=info["title"],
                author=info["owner_username"],
                time=datetime.fromisoformat(info["date_added"]),
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["description"],
            )
        case ("kemonoparty", _):
            # Kemono supports so many different source providers that it would be a pain to add
            # them all manually. In theory, they should all have the same structure of metadata.
            # Note that, just like coomer above, this also gets run for links to entire
            # profiles, which is somewhat janky due to treating the entire profile as one post.
            return Post(
                title=info["title"],
                author=info["username"],
                time=datetime.fromisoformat(info["published"]),
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["content"],
            )
        case ("lensdump", _):
            # TODO: They make you register in order to upload, and I can't be bothered right now
            raise NotImplementedError
        case ("lightroom", _):
            # TODO: Not entirely clear what content is downloaded/what those links look like
            raise NotImplementedError
        case ("motherless", "media"):
            return Post(
                title=info["title"],
                author=info["uploader"],
                time=info["date"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
            )
        case ("newgrounds", "image" | "media"):
            # Images and other media have different subcategories but the same metadata
            # structure
            return Post(
                title=info["title"],
                author=info["user"],
                time=info["date"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text="\n".join((info["comment"], info["description"])),
            )
        case ("pexels", "image"):
            # TODO: Needs browser cookies to download image, otherwise gets 403, but that 403 is
            # silent and the added Post is just without media. Should probably prompt user to
            # set cookie values themselves.
            return Post(
                title=info["title"],
                author=info["user"]["username"],
                time=datetime.fromisoformat(info["created_at"]),
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["description"],
            )
        case ("pinterest", "pin"):
            return Post(
                title=info["title"],
                author=info["closeup_attribution"]["username"],
                time=arrow.get(info["created_at"], arrow.FORMAT_RFC2822).datetime,
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["description_html"],
            )
        case ("pixiv", _):
            # TODO: Needs OAuth
            raise NotImplementedError
        case ("pornhub", _):
            # TODO: gallery-dl errors with "Unsupported URL"
            raise NotImplementedError
        case ("pornpics", "gallery"):
            return Post(
                title=info["title"],
                author=", ".join(info["models"]),
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
            )
        case ("raddle", "post"):
            # TODO: Text content is currently saved as an HTML file
            return Post(
                title=info["title"],
                author=info["username"],
                time=info["date"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
            )
        case ("realbooru", "post"):
            # TODO: Should probably look into grabbing from the original source
            return Post(
                title=info["title"],
                author=info["uploader"],
                time=info["date"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
            )
        case ("reddit", "submission"):
            return Post(
                title=info["title"],
                author=info["author"],
                time=info["date"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["selftext_html"],
            )
        case ("saint", "media"):
            # TODO: This doesn't give us a decent title
            return Post(
                title="untitled",
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["description"],
            )
        case ("saint", "album"):
            return Post(
                title=info["album_name"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["description"],
            )
        case ("scrolller", "post"):
            # TODO: Scrolller is just a reddit archive - should try downloading from original
            # Reddit post if it's still up
            return Post(
                title=info["title"],
                author=info["username"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
            )
        case ("soundgasm", "audio"):
            return Post(
                title=info["title"],
                author=info["user"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["description"],
            )
        case ("steamgriddb", "asset"):
            # This is basically a best guess for a probably-helpful title
            return Post(
                title=f"{info['game']['name']} - {info['style']} by {info['author']['name']}",
                author=info["author"]["name"],
                time=datetime.fromtimestamp(info["date"]),
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["notes"],
            )
        case ("telegraph", "gallery"):
            return Post(
                title=info["title"],
                author=info["author"],
                time=info["date"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["description"],
            )
        case ("tumblr", _):
            # TODO: Needs OAuth
            raise NotImplementedError
        case ("tumblrgallery", "post"):
            return Post(
                title=info["title"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
            )
        case ("twitter", "tweet"):
            return Post(
                title=content_to_title(info["content"]),
                author=info["author"]["name"],
                time=info["date"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["content"],
            )
        case ("unsplash", "image"):
            return Post(
                title=info["alt_description"],
                author=info["user"]["username"],
                time=datetime.fromisoformat(info["created_at"]),
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["description"],
            )
        case ("vsco", _):
            # TODO: Metadata is extremely sparse
            raise NotImplementedError
        case ("webmshare", "video"):
            return Post(
                title=info["title"],
                time=info["date"],
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
            )
        case ("xhamster", "gallery"):
            return Post(
                title=info["gallery"]["title"],
                author=info["user"]["name"],
                time=datetime.fromisoformat(info["gallery"]["date"]),
                source=f"{info['category']} {info['subcategory']}",
                source_url=url,
                text=info["gallery"]["description"],
            )
        case _:
            raise NotImplementedError

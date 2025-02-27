from datetime import datetime
from http import HTTPStatus
from io import BytesIO
from typing import Any

from flask import current_app, request, send_file
from werkzeug import Response

from . import db
from .downloader import download_post
from .models import Media, Post


@current_app.get("/media/<int:media_id>")
def show_media(media_id: int) -> Response:
    media = db.get_or_404(Media, media_id)
    return send_file(BytesIO(media.data), mimetype=media.mime_type, download_name=media.filename)


@current_app.get("/posts")
def index() -> list[dict[str, Any]]:
    posts = db.session.execute(db.select(Post).order_by(Post.time_added.desc())).scalars()
    return [post.to_dict() for post in posts]


@current_app.post("/posts/add")
def add_post() -> Response:
    post = download_post(request.form["url"])
    db.session.add(post)
    db.session.commit()
    return Response(status=HTTPStatus.NO_CONTENT)


@current_app.get("/posts/<int:post_id>")
def show_post(post_id: int) -> dict[str, Any]:
    post = db.get_or_404(Post, post_id)
    return post.to_dict()


@current_app.post("/posts/<int:post_id>/edit")
def edit_post(post_id: int) -> Response:
    post = db.get_or_404(Post, post_id)
    for key, val in request.form.items():
        new_val = val
        if key in ("time_created", "time_added"):
            new_val = datetime.fromisoformat(val)
        if hasattr(post, key):
            setattr(post, key, new_val)
    db.session.commit()
    return Response(status=HTTPStatus.NO_CONTENT)


@current_app.post("/posts/<int:post_id>/delete")
def delete_post(post_id: int) -> Response:
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return Response(status=HTTPStatus.NO_CONTENT)

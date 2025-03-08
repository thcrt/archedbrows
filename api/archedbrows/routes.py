from dataclasses import fields
from datetime import datetime
from http import HTTPStatus
from http.client import IM_A_TEAPOT
from io import BytesIO

from flask import current_app, make_response, request, send_file
from werkzeug import Response

from . import db
from .downloader import download_post
from .downloader.common import UnsupportedURLError
from .models import THUMBNAIL_TYPE, Media, Post

post_fields = {field.name: field for field in fields(Post)}


@current_app.route("/media/<int:media_id>")
def media(media_id: int) -> Response:
    media_obj = db.get_or_404(Media, media_id)
    return send_file(
        BytesIO(media_obj.data),
        download_name=media_obj.filename,
        mimetype=media_obj.mime_type,
    )


@current_app.route("/media/<int:media_id>/thumb")
def thumb(media_id: int) -> Response:
    media_obj = db.get_or_404(Media, media_id)
    if media_obj.thumb:
        return send_file(
            BytesIO(media_obj.thumb),
            download_name=f"thumb_{media_obj.filename}",
            mimetype=f"image/{THUMBNAIL_TYPE}",
        )
    return media(media_id=media_id)


@current_app.route("/posts", methods=["GET", "POST"])
def posts() -> Response:
    match request.method:
        case "GET":
            posts = db.session.execute(db.select(Post).order_by(Post.time_added.desc())).scalars()
            return make_response([post.to_dict() for post in posts])
        case "POST":
            if "auto" in request.form:
                try:
                    post = download_post(request.form["url"])
                except UnsupportedURLError:
                    return make_response(
                        {
                            "error": "UnsupportedURLError"
                        },
                        HTTPStatus.BAD_REQUEST
                    )
            else:
                post = Post(
                    source=request.form["source"],
                    source_url=request.form["source_url"],
                    title=request.form["title"],
                    author=request.form["author"],
                    time_created=(
                        datetime.fromisoformat(request.form["time_created"])
                        if request.form["time_created"]
                        else None
                    ),
                    text=request.form["text"],
                )
                for file in request.files.getlist("media"):
                    post.media.append(
                        Media(file.stream.read(), filename=file.filename, mime_type=file.mimetype)
                    )
            db.session.add(post)
            db.session.commit()
            return Response(status=HTTPStatus.CREATED)
        case _:
            return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)


@current_app.route("/posts/<int:post_id>", methods=["GET", "PATCH", "DELETE"])
def post(post_id: int) -> Response:
    match request.method:
        case "GET":
            post = db.get_or_404(Post, post_id)
            return make_response(post.to_dict())
        case "PATCH":
            post = db.get_or_404(Post, post_id)
            for key, val in request.form.items():
                new_val = val
                if key in ("time_created", "time_added"):
                    new_val = datetime.fromisoformat(val)
                if hasattr(post, key):
                    setattr(post, key, new_val)
            db.session.commit()
            return Response(status=HTTPStatus.NO_CONTENT)
        case "DELETE":
            post = db.get_or_404(Post, post_id)
            db.session.delete(post)
            db.session.commit()
            return Response(status=HTTPStatus.NO_CONTENT)
        case _:
            return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)


@current_app.route("/teapot")
def teapot() -> Response:
    return Response("🫖", status=IM_A_TEAPOT)

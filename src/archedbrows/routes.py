from io import BytesIO

from flask import current_app, redirect, render_template, request, send_file, url_for
from werkzeug import Response

from . import db
from .downloader import download_post
from .models import Media, Post


@current_app.get("/")
def index() -> str:
    posts = db.session.execute(db.select(Post).order_by(Post.time_added.desc())).scalars()
    return render_template("index.html.jinja", posts=posts)


@current_app.get("/posts/<int:post_id>")
def show_post(post_id: int) -> str:
    post = db.get_or_404(Post, post_id)
    return render_template("post.html.jinja", post=post)


@current_app.get("/media/<int:media_id>")
def show_media(media_id: int) -> Response:
    media = db.get_or_404(Media, media_id)
    return send_file(BytesIO(media.data), mimetype=media.mime_type, download_name=media.filename)


@current_app.post("/add")
def add() -> Response:
    post = download_post(request.form["url"])
    db.session.add(post)
    db.session.commit()
    return redirect(url_for("index"))

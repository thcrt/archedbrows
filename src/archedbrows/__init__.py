import io

import flask as f
from werkzeug import Response

from .database import Media, Post, db
from .downloader.gallerydl import download_post


def create_app() -> f.Flask:
    app = f.Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.get("/")
    def index() -> str:
        posts = db.session.execute(db.select(Post).order_by(Post.time.desc())).scalars()
        return f.render_template("index.html.jinja", posts=posts)

    @app.get("/posts/<int:post_id>")
    def show_post(post_id: int) -> str:
        post = db.get_or_404(Post, post_id)
        return f.render_template("post.html.jinja", post=post)

    @app.get("/media/<int:media_id>")
    def show_media(media_id: int) -> Response:
        media = db.get_or_404(Media, media_id)
        return f.send_file(
            io.BytesIO(media.data), mimetype=media.mime_type, download_name=media.filename
        )

    @app.post("/add")
    def add() -> Response:
        post = download_post(f.request.form["url"])
        db.session.add(post)
        db.session.commit()
        return f.redirect(f.url_for("index"))

    return app

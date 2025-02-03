import io

import flask as f
from werkzeug import Response

from .database import Media, Post, db
from .downloader import Downloader


def create_app() -> f.Flask:
    app = f.Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

    db.init_app(app)
    with app.app_context():
        db.create_all()
    downloader = Downloader()

    @app.get("/")
    def index() -> str:
        posts = db.session.execute(db.select(Post)).scalars()
        return f.render_template("index.html.jinja", posts=posts)

    @app.get("/media/<int:media_id>")
    def show_media(media_id: int) -> Response:
        media = db.get_or_404(Media, media_id)
        return f.send_file(io.BytesIO(media.data), mimetype=media.mime_type)

    @app.post("/add")
    def add() -> Response:
        post = downloader.download_post(f.request.form["url"])
        db.session.add(post)
        db.session.commit()
        return f.redirect(f.url_for("index"))

    return app

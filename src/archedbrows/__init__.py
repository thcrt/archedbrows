import flask as f

from .posts import PostManager


def create_app() -> f.Flask:
    app = f.Flask(__name__)

    pm = PostManager.with_dummy_data()

    @app.route("/")
    def index() -> str:
        return f.render_template("index.html.jinja", posts=pm.posts)

    return app

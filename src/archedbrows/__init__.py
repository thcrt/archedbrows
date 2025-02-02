import flask as f


def create_app() -> f.Flask:
    app = f.Flask(__name__)

    @app.route("/")
    def index() -> str:
        return f.render_template("index.html.jinja")

    return app

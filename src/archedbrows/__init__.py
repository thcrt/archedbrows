import flask as f


def create_app() -> f.Flask:
    app = f.Flask(__name__)

    @app.route("/")
    def index() -> str:
        return "Hello, world!"

    return app

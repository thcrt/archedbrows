import flask as f
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_vite import Vite  # pyright: ignore[reportMissingTypeStubs]
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
vite = Vite()


def create_app() -> f.Flask:
    app = f.Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    app.config["VITE_AUTO_INSERT"] = True

    db.init_app(app)
    migrate.init_app(app, db)
    vite.init_app(app)

    with app.app_context():
        from . import routes  # noqa: F401 # pyright: ignore[reportUnusedImport]

    from .models import Media, Post  # noqa: F401 # pyright: ignore[reportUnusedImport]

    return app

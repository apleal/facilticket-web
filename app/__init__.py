import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, static_folder="../static", template_folder="templates")
    app.config.from_mapping(
        PUBLIC_BASE_URL=os.getenv("PUBLIC_BASE_URL", "https://facilticket.es").rstrip("/"),
        REGISTRATION_URL=os.getenv(
            "REGISTRATION_URL", "https://app.facilticket.es/registro"
        ),
        LOGIN_URL=os.getenv("LOGIN_URL", ""),
        CONTACT_EMAIL=os.getenv("CONTACT_EMAIL", ""),
        APP_ENV=os.getenv("APP_ENV", "development"),
    )
    if test_config:
        app.config.update(test_config)

    from .routes import pages

    app.register_blueprint(pages)
    return app


from flask import Flask
import pytest


@pytest.fixture(scope="session")
def minimal_app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app


"""Pytest fixtures."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app
from app.config import TestConfig
from app.extensions import db
from app.models import User, UserRole


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        admin = User(username="admin", full_name="Admin", role=UserRole.ADMIN)
        admin.set_password("Admin123!")
        officer = User(username="officer", full_name="Officer", role=UserRole.LEGAL_OFFICER)
        officer.set_password("Officer123!")
        db.session.add_all([admin, officer])
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

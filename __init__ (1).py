"""Application configuration module."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Config:
    """Base config with secure defaults."""

    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/legal_tracker"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    REMINDER_DAYS: int = int(os.getenv("REMINDER_DAYS", "7"))


class TestConfig(Config):
    """Test config using SQLite in-memory db for fast tests."""

    TESTING: bool = True
    WTF_CSRF_ENABLED: bool = False
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"

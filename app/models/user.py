"""User model and role definitions."""
from __future__ import annotations

from enum import Enum

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class UserRole(str, Enum):
    """Supported application roles."""

    ADMIN = "Admin"
    LEGAL_OFFICER = "Legal Officer"
    REVIEWER = "Reviewer"


class User(UserMixin, db.Model):
    """Application user model."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    assigned_tasks = db.relationship("ComplianceTask", back_populates="assignee", lazy=True)
    activity_logs = db.relationship("ActivityLog", back_populates="actor", lazy=True)

    def set_password(self, password: str) -> None:
        """Hash and persist password securely."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Validate password against stored hash."""
        return check_password_hash(self.password_hash, password)

    def has_role(self, *roles: UserRole) -> bool:
        """Check whether user role is one of provided roles."""
        return self.role in roles

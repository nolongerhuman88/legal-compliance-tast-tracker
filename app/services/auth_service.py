"""Authentication and authorization helpers."""
from __future__ import annotations

from functools import wraps
from typing import Callable

from flask import abort
from flask_login import current_user

from app.models import UserRole


def roles_required(*roles: UserRole) -> Callable:
    """Protect endpoint by ensuring current user matches expected roles."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if not current_user.has_role(*roles):
                abort(403)
            return func(*args, **kwargs)

        return wrapper

    return decorator

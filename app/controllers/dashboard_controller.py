"""Dashboard routes."""
from __future__ import annotations

from flask import Blueprint, current_app, render_template
from flask_login import login_required

from app.services.task_service import TaskService

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    """Show compliance dashboard summary metrics."""
    metrics = TaskService.dashboard_metrics()
    due_soon_tasks = TaskService.due_soon_tasks(current_app.config["REMINDER_DAYS"])
    return render_template("dashboard/index.html", metrics=metrics, due_soon_tasks=due_soon_tasks)

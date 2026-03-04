"""Compliance task routes."""
from __future__ import annotations

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import TaskForm
from app.models import ComplianceTask, RiskLevel, TaskStatus, User, UserRole
from app.services.auth_service import roles_required
from app.services.task_service import TaskService

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def _populate_assignee_choices(form: TaskForm) -> None:
    users = User.query.order_by(User.full_name.asc()).all()
    form.assigned_to.choices = [(user.id, f"{user.full_name} ({user.role.value})") for user in users]


def _extract_task_data(form: TaskForm) -> dict:
    return {
        "title": form.title.data,
        "description": form.description.data,
        "regulation_reference": form.regulation_reference.data,
        "risk_level": RiskLevel(form.risk_level.data),
        "due_date": form.due_date.data,
        "status": TaskStatus(form.status.data),
        "assigned_to": form.assigned_to.data,
    }


@task_bp.route("/")
@login_required
def list_tasks():
    """List tasks with reminder highlighting."""
    query = ComplianceTask.query.order_by(ComplianceTask.due_date.asc())
    status_filter = request.args.get("status")
    if status_filter:
        query = query.filter_by(status=TaskStatus(status_filter))
    tasks = query.all()
    due_soon_ids = {task.id for task in TaskService.due_soon_tasks(current_app.config["REMINDER_DAYS"])}
    return render_template("tasks/list.html", tasks=tasks, due_soon_ids=due_soon_ids, statuses=TaskStatus)


@task_bp.route("/create", methods=["GET", "POST"])
@login_required
@roles_required(UserRole.ADMIN, UserRole.LEGAL_OFFICER)
def create_task():
    form = TaskForm()
    _populate_assignee_choices(form)
    if form.validate_on_submit():
        TaskService.create_task(_extract_task_data(form), current_user)
        flash("Task created successfully.", "success")
        return redirect(url_for("tasks.list_tasks"))
    return render_template("tasks/form.html", form=form, form_title="Create Task")


@task_bp.route("/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
@roles_required(UserRole.ADMIN, UserRole.LEGAL_OFFICER, UserRole.REVIEWER)
def edit_task(task_id: int):
    task = ComplianceTask.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    _populate_assignee_choices(form)
    if form.validate_on_submit():
        TaskService.update_task(task, _extract_task_data(form), current_user)
        flash("Task updated successfully.", "success")
        return redirect(url_for("tasks.list_tasks"))
    form.risk_level.data = task.risk_level.value
    form.status.data = task.status.value
    form.assigned_to.data = task.assigned_to
    return render_template("tasks/form.html", form=form, form_title="Edit Task")


@task_bp.route("/<int:task_id>/delete", methods=["POST"])
@login_required
@roles_required(UserRole.ADMIN)
def delete_task(task_id: int):
    task = ComplianceTask.query.get_or_404(task_id)
    TaskService.delete_task(task, current_user)
    flash("Task deleted.", "warning")
    return redirect(url_for("tasks.list_tasks"))


@task_bp.route("/<int:task_id>/activity")
@login_required
def task_activity(task_id: int):
    task = ComplianceTask.query.get_or_404(task_id)
    activities = task.activities
    return render_template("tasks/activity.html", task=task, activities=activities)

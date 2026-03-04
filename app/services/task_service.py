"""Business logic for compliance task operations."""
from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from sqlalchemy import func

from app.extensions import db
from app.models import ActivityLog, ComplianceTask, RiskLevel, TaskStatus, User


class TaskService:
    """Encapsulates task business rules."""

    @staticmethod
    def create_task(data: dict[str, Any], actor: User) -> ComplianceTask:
        task = ComplianceTask(**data)
        db.session.add(task)
        db.session.flush()
        TaskService._log(task.id, actor.id, "CREATE", f"Task '{task.title}' created")
        db.session.commit()
        return task

    @staticmethod
    def update_task(task: ComplianceTask, data: dict[str, Any], actor: User) -> ComplianceTask:
        before = {"status": task.status.value, "risk_level": task.risk_level.value, "assignee": task.assigned_to}
        for key, value in data.items():
            setattr(task, key, value)
        db.session.flush()
        after = {"status": task.status.value, "risk_level": task.risk_level.value, "assignee": task.assigned_to}
        details = f"Task '{task.title}' updated | before={before} after={after}"
        TaskService._log(task.id, actor.id, "UPDATE", details)
        db.session.commit()
        return task

    @staticmethod
    def delete_task(task: ComplianceTask, actor: User) -> None:
        TaskService._log(task.id, actor.id, "DELETE", f"Task '{task.title}' deleted")
        db.session.delete(task)
        db.session.commit()

    @staticmethod
    def dashboard_metrics() -> dict[str, Any]:
        status_counts = (
            db.session.query(ComplianceTask.status, func.count(ComplianceTask.id))
            .group_by(ComplianceTask.status)
            .all()
        )
        risk_counts = (
            db.session.query(ComplianceTask.risk_level, func.count(ComplianceTask.id))
            .group_by(ComplianceTask.risk_level)
            .all()
        )
        overdue_tasks = ComplianceTask.query.filter(
            ComplianceTask.due_date < date.today(), ComplianceTask.status != TaskStatus.CLOSED
        ).count()
        return {
            "status_counts": {status.value: count for status, count in status_counts},
            "risk_counts": {risk.value: count for risk, count in risk_counts},
            "overdue_tasks": overdue_tasks,
        }

    @staticmethod
    def due_soon_tasks(reminder_days: int) -> list[ComplianceTask]:
        target_date = date.today() + timedelta(days=reminder_days)
        return (
            ComplianceTask.query.filter(
                ComplianceTask.status != TaskStatus.CLOSED,
                ComplianceTask.due_date <= target_date,
                ComplianceTask.due_date >= date.today(),
            )
            .order_by(ComplianceTask.due_date.asc())
            .all()
        )

    @staticmethod
    def _log(task_id: int, actor_id: int, action: str, details: str) -> None:
        log = ActivityLog(task_id=task_id, actor_id=actor_id, action=action, details=details)
        db.session.add(log)

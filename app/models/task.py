"""Compliance task and audit activity models."""
from __future__ import annotations

from enum import Enum
from datetime import date

from app.extensions import db


class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class TaskStatus(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    PENDING_REVIEW = "Pending Review"
    CLOSED = "Closed"


class ComplianceTask(db.Model):
    """Main task entity."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    regulation_reference = db.Column(db.String(255), nullable=False)
    risk_level = db.Column(db.Enum(RiskLevel), nullable=False, default=RiskLevel.LOW)
    due_date = db.Column(db.Date, nullable=False, index=True)
    status = db.Column(db.Enum(TaskStatus), nullable=False, default=TaskStatus.OPEN)
    assigned_to = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now(), nullable=False)

    assignee = db.relationship("User", back_populates="assigned_tasks")
    activities = db.relationship("ActivityLog", back_populates="task", lazy=True, cascade="all, delete-orphan")

    @property
    def is_overdue(self) -> bool:
        """Check if open task has crossed due date."""
        return self.status != TaskStatus.CLOSED and self.due_date < date.today()


class ActivityLog(db.Model):
    """Audit trail for task changes."""

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("compliance_task.id"), nullable=False, index=True)
    actor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    details = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    task = db.relationship("ComplianceTask", back_populates="activities")
    actor = db.relationship("User", back_populates="activity_logs")

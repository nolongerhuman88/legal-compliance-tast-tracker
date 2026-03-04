from datetime import date, timedelta

from app.extensions import db
from app.models import ActivityLog, ComplianceTask, RiskLevel, TaskStatus, User
from app.services.task_service import TaskService


def test_create_task_creates_activity_log(app):
    with app.app_context():
        actor = User.query.filter_by(username="admin").first()
        assignee = User.query.filter_by(username="officer").first()
        TaskService.create_task(
            {
                "title": "Task A",
                "description": "Desc",
                "regulation_reference": "Reg A",
                "risk_level": RiskLevel.MEDIUM,
                "due_date": date.today() + timedelta(days=4),
                "status": TaskStatus.OPEN,
                "assigned_to": assignee.id,
            },
            actor,
        )

        assert ComplianceTask.query.count() == 1
        assert ActivityLog.query.count() == 1


def test_due_soon_tasks_filters_correctly(app):
    with app.app_context():
        assignee = User.query.filter_by(username="officer").first()
        db.session.add_all(
            [
                ComplianceTask(
                    title="Soon",
                    description="Soon",
                    regulation_reference="Reg",
                    risk_level=RiskLevel.HIGH,
                    due_date=date.today() + timedelta(days=2),
                    status=TaskStatus.OPEN,
                    assigned_to=assignee.id,
                ),
                ComplianceTask(
                    title="Later",
                    description="Later",
                    regulation_reference="Reg",
                    risk_level=RiskLevel.LOW,
                    due_date=date.today() + timedelta(days=20),
                    status=TaskStatus.OPEN,
                    assigned_to=assignee.id,
                ),
            ]
        )
        db.session.commit()

        tasks = TaskService.due_soon_tasks(7)
        assert len(tasks) == 1
        assert tasks[0].title == "Soon"

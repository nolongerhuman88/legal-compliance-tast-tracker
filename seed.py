"""Seed script for development data."""
from __future__ import annotations

from datetime import date, timedelta

from dotenv import load_dotenv

from app import create_app
from app.extensions import db
from app.models import ComplianceTask, RiskLevel, TaskStatus, User, UserRole

load_dotenv()
app = create_app()


def run_seed() -> None:
    """Populate database with sample users and tasks."""
    with app.app_context():
        db.create_all()
        if User.query.count() == 0:
            admin = User(username="admin", full_name="System Admin", role=UserRole.ADMIN)
            admin.set_password("Admin123!")
            officer = User(username="officer", full_name="Legal Officer", role=UserRole.LEGAL_OFFICER)
            officer.set_password("Officer123!")
            reviewer = User(username="reviewer", full_name="Compliance Reviewer", role=UserRole.REVIEWER)
            reviewer.set_password("Reviewer123!")
            db.session.add_all([admin, officer, reviewer])
            db.session.flush()

            db.session.add_all(
                [
                    ComplianceTask(
                        title="Review AML policy",
                        description="Annual review for anti-money laundering policy.",
                        regulation_reference="POJK 12/2023",
                        risk_level=RiskLevel.HIGH,
                        due_date=date.today() + timedelta(days=5),
                        status=TaskStatus.IN_PROGRESS,
                        assigned_to=officer.id,
                    ),
                    ComplianceTask(
                        title="Submit quarterly report",
                        description="Submit compliance report to regulator.",
                        regulation_reference="SEOJK 7/2024",
                        risk_level=RiskLevel.CRITICAL,
                        due_date=date.today() - timedelta(days=2),
                        status=TaskStatus.OPEN,
                        assigned_to=reviewer.id,
                    ),
                ]
            )
            db.session.commit()
            print("Seed data inserted.")
        else:
            print("Seed skipped: users already exist.")


if __name__ == "__main__":
    run_seed()

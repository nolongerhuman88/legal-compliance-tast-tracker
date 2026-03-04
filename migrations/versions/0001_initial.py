"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2026-03-04
"""
from alembic import op
import sqlalchemy as sa


revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('full_name', sa.String(length=120), nullable=False),
        sa.Column('role', sa.Enum('ADMIN', 'LEGAL_OFFICER', 'REVIEWER', name='userrole'), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)

    op.create_table(
        'compliance_task',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('regulation_reference', sa.String(length=255), nullable=False),
        sa.Column('risk_level', sa.Enum('LOW', 'MEDIUM', 'HIGH', 'CRITICAL', name='risklevel'), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=False),
        sa.Column('status', sa.Enum('OPEN', 'IN_PROGRESS', 'PENDING_REVIEW', 'CLOSED', name='taskstatus'), nullable=False),
        sa.Column('assigned_to', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['assigned_to'], ['user.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_compliance_task_due_date'), 'compliance_task', ['due_date'], unique=False)
    op.create_index(op.f('ix_compliance_task_title'), 'compliance_task', ['title'], unique=False)

    op.create_table(
        'activity_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('actor_id', sa.Integer(), nullable=False),
        sa.Column('action', sa.String(length=50), nullable=False),
        sa.Column('details', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['actor_id'], ['user.id']),
        sa.ForeignKeyConstraint(['task_id'], ['compliance_task.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_activity_log_task_id'), 'activity_log', ['task_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_activity_log_task_id'), table_name='activity_log')
    op.drop_table('activity_log')
    op.drop_index(op.f('ix_compliance_task_title'), table_name='compliance_task')
    op.drop_index(op.f('ix_compliance_task_due_date'), table_name='compliance_task')
    op.drop_table('compliance_task')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.execute('DROP TYPE taskstatus')
    op.execute('DROP TYPE risklevel')
    op.execute('DROP TYPE userrole')

"""WTForms declarations."""
from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import DateField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

from app.models import RiskLevel, TaskStatus, UserRole


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Login")


class TaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=150)])
    description = TextAreaField("Description", validators=[DataRequired()])
    regulation_reference = StringField("Regulation Reference", validators=[DataRequired(), Length(max=255)])
    risk_level = SelectField(
        "Risk Level",
        choices=[(choice.value, choice.value) for choice in RiskLevel],
        validators=[DataRequired()],
    )
    due_date = DateField("Due Date", validators=[DataRequired()], format="%Y-%m-%d")
    status = SelectField(
        "Status",
        choices=[(choice.value, choice.value) for choice in TaskStatus],
        validators=[DataRequired()],
    )
    assigned_to = SelectField("Assigned To", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Save")


ROLE_CHOICES = [(role.value, role.value) for role in UserRole]

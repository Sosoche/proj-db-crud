import re

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length, ValidationError


class UserForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=50)]
    )
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=100)])

    def validate_username(self, username: StringField) -> None:
        """
        Проверяет формат имени пользователя.
        """
        if not re.match(r"^[a-zA-Z0-9_]+$", str(username.data)):
            raise ValidationError(
                "Username must contain only latin letters, numbers, and underscores."
            )

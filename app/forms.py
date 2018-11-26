from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import Required, Email
from wtforms.fields.html5 import EmailField


class SigninForm(FlaskForm):
    """Accepts a nickname and a room."""
    username = StringField('Username', validators=[Required()])
    pwd = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Signin')

class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[Required()])
    pwd = PasswordField("Password", validators=[Required()])
    first_name = StringField("first_name", validators=[Required()])
    last_name = StringField("last_name", validators=[Required()])
    email = EmailField("Email", validators=[Email()])
    admin_level = RadioField('User Type', choices=[("0","Student"),
                            ("1" ,"Parent/Guardian"), ("2", "Teacher")])
    submit = SubmitField("Sign Up")

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,EmailField,SelectField,URLField,IntegerField,DateField,TextAreaField
from wtforms import DateTimeLocalField,FileField,TelField,TimeField,DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from flask_wtf.file import FileField,FileRequired,FileAllowed

class DpForm(FlaskForm):
    photo=FileField(validators=[FileRequired(),FileAllowed(['jpg','png','jpeg'],'ONLY IMAGES ARE ALLOWED')])
    uploadbtn=SubmitField('Upload Picture')

class RegistrationForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired('Please enter your first name')])
    lname = StringField('Last Name', validators=[DataRequired('Please enter your last name')])
    email = EmailField('Email', validators=[DataRequired('Email is required'), Email('Please enter a valid email')])
    phone = TelField('Phone Number')
    password = PasswordField('Password', validators=[DataRequired('Password is required')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('login')



class ChatForm(FlaskForm):
    prompt = StringField(
        'Message',
        validators=[DataRequired(), Length(min=1, max=500)],
        render_kw={"placeholder": "Type your message...", "autocomplete": "off"}
    )
    submit = SubmitField('Send')

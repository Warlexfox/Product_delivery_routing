from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange

class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email(message='Invalid email format')])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Log-in')

class RegisterForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email(message='Invalid email format')])
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password:', validators=[
        DataRequired(), EqualTo('password', message='The passwords must match')
    ])
    submit = SubmitField('Register')

class LocationForm(FlaskForm):
    country = StringField('Country', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    timeframe = StringField('Timeframe', validators=[DataRequired()])
    submit_location = SubmitField('Save Location')

class UploadLocationsForm(FlaskForm):
    file = FileField('Choose file', validators=[DataRequired()])
    submit_upload = SubmitField('Upload')

class RenameRouteForm(FlaskForm):
    name = StringField('New Route Name', validators=[DataRequired()])
    submit = SubmitField('Rename')

class EditDriverPriorityForm(FlaskForm):
    priority = IntegerField('Driver Priority', validators=[DataRequired(), NumberRange(min=1, message='Priority must be >= 1')])
    submit = SubmitField('Save')

class DriverForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    tel_num = IntegerField('Phone number', validators=[DataRequired()])
    depot_address = StringField('Depot Address', validators=[DataRequired()])
    priority = IntegerField('Priority', validators=[DataRequired(), NumberRange(min=1, message='Priority must be >= 1')])
    submit_driver = SubmitField('Save Driver')

class UploadDriversForm(FlaskForm):
    file = FileField('Choose file', validators=[DataRequired()])
    submit_upload_drivers = SubmitField('Upload Drivers')

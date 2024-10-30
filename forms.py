from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, FileField
from wtforms.validators import DataRequired

class LocationForm(FlaskForm):
    address = StringField('Adrese', validators=[DataRequired()])
    demand = FloatField('Pieprasījums', validators=[DataRequired()])
    ready_time = FloatField('Laika loga sākums', validators=[DataRequired()])
    due_time = FloatField('Laika loga beigas', validators=[DataRequired()])
    service_time = FloatField('Apkalpošanas laiks', validators=[DataRequired()])
    submit = SubmitField('Pievienot lokāciju')

class UploadLocationsForm(FlaskForm):
    file = FileField('Izvēlieties JSON failu ar lokācijām', validators=[DataRequired()])
    submit = SubmitField('Augšupielādēt lokācijas')

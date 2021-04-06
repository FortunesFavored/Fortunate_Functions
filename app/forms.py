from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired

class Equation(FlaskForm):
    equation = StringField('Your Awesome Equation')
    submit = SubmitField()
class Variables(FlaskForm):
    slope = FloatField('Slope')
    exponent = FloatField('Exponent')
    submit = SubmitField()

class DataFile(FlaskForm):
    file = FileField('File')
    submit = SubmitField('Submit')
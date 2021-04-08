from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired

class Equation(FlaskForm):
    equation = StringField('Your Awesome Equation')
    submit = SubmitField()
class LineVariables(FlaskForm):
    slope = FloatField('Slope')
    intercept = FloatField('intercept')
    submit = SubmitField()

class BellVariables(FlaskForm):
    sq_a = FloatField('A')
    sq_b = FloatField('B')
    sq_c = FloatField('C')
    submit = SubmitField()

class DataFile(FlaskForm):
    file = FileField('File')
    submit = SubmitField('Submit')
from flask_wtf import Form
from wtforms import StringField, DateField
from wtforms.validators import DataRequired


class EntryForm(Form):
    '''Form to create new entry'''
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    spent = StringField('Time spent', validators=[DataRequired()])
    learned = StringField('What did I learn?', validators=[DataRequired()])
    resources = StringField('Resources', validators=[DataRequired()])

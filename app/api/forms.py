# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, SubmitField, \
    PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from ..main.forms import CommentForm

class TaskCommonForm(FlaskForm):
    title = StringField(u'标题', validators=[DataRequired(), Length(1, 64)])

class TaskSubmitForm(TaskCommonForm):
    content = TextAreaField(u'内容')

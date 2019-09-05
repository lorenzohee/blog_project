# coding:utf-8
from wtforms import SelectField, StringField, TextAreaField, SubmitField, \
    PasswordField, Form
from wtforms.validators import DataRequired, Length, Email, EqualTo

class TaskCommonForm(Form):
    title = StringField(u'标题')
    content = TextAreaField(u'内容')

class TaskSubmitForm(TaskCommonForm):
    content = TextAreaField(u'内容')

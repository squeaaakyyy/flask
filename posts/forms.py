from wtforms import Form, StringField, TextAreaField
from wtforms.validators import InputRequired


class PostForm(Form):
    title = StringField('Title', validators=[InputRequired()])
    body = TextAreaField('Body', validators=[InputRequired()])
    tag = StringField('Tag', validators=[InputRequired()])


class PostEditForm(Form):
    title = StringField('Title', validators=[InputRequired()])
    body = TextAreaField('Body', validators=[InputRequired()])


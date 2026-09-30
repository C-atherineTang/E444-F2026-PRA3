from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField(
    'What is your email?',
    validators=[DataRequired()],
    render_kw={'type': 'email'}
)
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()

    if form.validate_on_submit():
        email = form.email.data

        if 'utoronto' in email:
            old_name = session.get('name')

            if old_name is not None and old_name != form.name.data:
                flash('Looks like you have changed your name!')

            session['name'] = form.name.data
            session['email'] = email

            return redirect(url_for('index'))

        else:
            flash('Please fill in a UofT email.')

    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        email=session.get('email')
    )
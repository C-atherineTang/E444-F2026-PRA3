from flask import Flask, render_template, session, redirect, url_for, flash, request
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

            return redirect(url_for('chat_page'))

        else:
            flash('Please fill in a UofT email.')

    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        email=session.get('email')
    )

@app.route('/chat')
def chat_page():
    if 'name' not in session:
        return redirect(url_for('index'))

    return render_template('chat.html', name=session['name'])


@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']

    if 'my name is' in message.lower():
        name = message.lower().split('my name is', 1)[1].strip()

        if name:
            session['chat_name'] = name
            reply = f'Nice to meet you, {name}!'

        else:
            reply = "I didn't catch your name."

    elif 'what is my name' in message.lower():
        if 'chat_name' in session:
            reply = f"Your name is {session['chat_name']}."

        else:
            reply = "I don't know your name yet."

    elif 'hello' in message.lower():
        reply = 'Hello!'

    else:
        reply = "I don't understand."

    return {'reply': reply}


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
# app/main.py

import datetime
import logging
logging.basicConfig(filename='record.log', level=logging.DEBUG)

from fastapi import FastAPI, Request
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, render_template, abort, request, url_for, flash, redirect
from markupsafe import Markup

from app.forms import CourseForm

from app.db import database, User

# init FastAPI app and Flask app
app = FastAPI(title="FastAPI, Docker, and Traefik")
flask_app = Flask(__name__)

# from flask.logging import default_handler
# flask_app.logger.removeHandler(default_handler)

flask_app.config['SECRET_KEY'] = 'ABCDEF-GHIJKL'

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]

courses_list = [{
    'title': 'Python 101',
    'description': 'Learn Python basics',
    'price': 34,
    'available': True,
    'level': 'Beginner'
    }]


# mount Flask on FastAPI
app.mount("/flask",WSGIMiddleware(flask_app))

@flask_app.get('/blog')
def blog_page():
  return "Blog Section from Flask"

@flask_app.route('/')
def hello():
    return render_template('index.html', utc_dt=datetime.datetime.utcnow())

@flask_app.route('/about/')
def about():
    return render_template('about.html')

@flask_app.route('/courses/')
def courses():
    return render_template('courses.html', courses_list=courses_list)

@flask_app.route('/comments/')
def comments():
    comments = ['This is the first comment.',
                'This is the second comment.',
                'This is the third comment.',
                'This is the fourth comment.'
                ]

    return render_template('comments.html', comments=comments)

@flask_app.route('/other_comments/')
def other_comments():
    comments = ['This is the very fifth comment.',
                'This is the very sixth comment.',
                'This is the very seventh comment.',
                'This is the very eighth comment.'
                ]

    return render_template('other_comments.html', comments=comments)

@flask_app.route('/messages/<int:idx>')
def message(idx):
    flask_app.logger.info('Building the messages list...')
    # messages = ['Message Zero', 'Message One', 'Message Two']
    try:
        flask_app.logger.debug('Get message with index: {}'.format(idx))
        return render_template('message.html', message=messages[idx])
    except IndexError:
        flask_app.logger.debug('Get message with index: {}'.format(idx))
        abort(404)

@flask_app.route('/500')
def error500():
    abort(500)

@flask_app.route('/create/', methods=('GET', 'POST'))
def create_message():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            messages.append({'title': title, 'content': content})
            flask_app.logger.debug(f"appended to messages.  now {str(len(messages)+1)} of them.")
            return redirect(url_for('hello'))
        
    return render_template('create.html')

@flask_app.route('/courseform', methods=('GET', 'POST'))
def courseform():
    form = CourseForm()
    if form.validate_on_submit():
        flask_app.logger.debug("Here i am.")
        courses_list.append({'title': form.title.data,
                             'description': form.description.data,
                             'price': form.price.data,
                             'available': form.available.data,
                             'level': form.level.data
                             })
        return redirect(url_for('courses'))
    return render_template('courseform.html', form=form)


@flask_app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@flask_app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.get("/fastapi")
async def read_root():
    return await User.objects.all()

@app.get("/about")
async def about_page():
  return "This is the About Page"

@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    await User.objects.get_or_create(email="test@test.com")

@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()

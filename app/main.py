# app/main.py

import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, render_template

from app.db import database, User

# init FastAPI app and Flask app
app = FastAPI(title="FastAPI, Docker, and Traefik")
flask_app = Flask(__name__)

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



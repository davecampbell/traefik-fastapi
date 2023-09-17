# app/main.py

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

@app.get("/")
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



#app.py

import os
import pathlib
import requests
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from app import app, db
from app.models import User, Car


app.secret_key = "fleetmanagermararouta"  #it is necessary to set a password when dealing with OAuth 2.0
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  #this is to set our environment to https because OAuth 2.0 only supports https environments

GOOGLE_CLIENT_ID = "320557972351-45t22fcflec03q8er86pp93aqdike9uh.apps.googleusercontent.com"  #enter your client id you got from Google console


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Car': Car}
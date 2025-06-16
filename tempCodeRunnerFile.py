from flask import Flask
from models import db
from auth import BP_auth
from routes import BP
from scheduler import start_scheduler

app = Flask(__name__)
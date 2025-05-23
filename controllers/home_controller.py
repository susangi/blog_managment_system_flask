from flask import Blueprint, render_template
from db import dbConnection

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():

    return render_template('index.html')




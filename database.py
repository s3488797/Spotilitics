
from falsk import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_databse():
    app = Flask(__name__)
    

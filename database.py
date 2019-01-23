
from falsk import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_databse():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)
    with app.app_context():

#Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(255))
    display_name = db.Column(db.String(255))
    joined = db.Column(db.DateTime())
    last_check = db.Column(db.DateTime())
    listens = db.Column(db.Integer)
    auth_token = db.Column(db.String(255))
    refresh_token = db.Column(db.)

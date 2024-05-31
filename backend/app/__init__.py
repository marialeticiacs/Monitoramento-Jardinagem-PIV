from flask import Flask
from pymongo import MongoClient
from flask_jwt_extended import JWTManager
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

client = MongoClient(app.config['MONGO_URI'])
db = client['User']

jwt = JWTManager(app)

from app.routes import routes as main_routes
app.register_blueprint(main_routes, url_prefix='/api')

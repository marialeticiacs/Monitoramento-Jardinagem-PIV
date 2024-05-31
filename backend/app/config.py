import os
from dotenv import load_dotenv
import certifi

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'
    MONGO_USERNAME = os.getenv('MONGO_USERNAME')
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
    MONGO_CLUSTER_URL = os.getenv('MONGO_CLUSTER_URL')
    MONGO_URI = "mongodb+srv://marialeticia:mleticia2005@cluster-piv.rr2y51m.mongodb.net/DB_PIV?retryWrites=true&w=majority&tlsCAFile={}".format(certifi.where())


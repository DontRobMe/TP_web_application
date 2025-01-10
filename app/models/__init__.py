from flask_pymongo import PyMongo
from config import Config

mongo = PyMongo()

def init_db(app):
    mongo.init_app(app, uri=Config.MONGO_URI)


def get_sondage_collection():
    return mongo.db.sondages


def get_reponse_collection():
    return mongo.db.reponses

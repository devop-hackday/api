from flask import Flask, request, jsonify, abort, redirect
import logging
from logging.handlers import RotatingFileHandler

api = Flask(__name__)
api.config.from_object('config')
# db = SQLAlchemy(api)

handler = RotatingFileHandler('api.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
api.logger.addHandler(handler)

from papi import upload, list, landing, api

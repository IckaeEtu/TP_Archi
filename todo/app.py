from flask import Flask
from flask_cors import CORS
app = Flask(__name__)

cors = CORS (app, resources={r"/todo/api/v1.0/*":{"origins":"*" }})
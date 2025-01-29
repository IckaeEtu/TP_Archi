from Questionnaire.app import app
from Questionnaire.models import db

with app.app_context():
    db.create_all()
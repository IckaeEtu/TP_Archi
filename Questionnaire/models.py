# Version fonctionnelle qui ne gère pas les types de questions
from .app import app,db

class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Questionnaire (%d) %s>" % (self.id, self.name)

    def to_json(self):
        json = {
            'id': self.id,
            'name': self.name
        }
        return json

class Question(db.Model):

    def __init__(self, title, questionType, questionnaire_id):
        self.title = title
        self.questionType = questionType
        self.questionnaire_id = questionnaire_id


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    questionType = db.Column(db.String(120))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))
    questionnaire = db.relationship("Questionnaire", backref=db.backref(
        "questions", lazy="dynamic"))


    def to_json(self):
        json = {
            'id': self.id,
            'title': self.title,
            'questionType': self.questionType,
            'questionnaire_id': self.questionnaire_id
        }
        return json

# Versionqui gère les types de questions
# from .app import app, db

# class Questionnaire(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))

#     def __init__(self, name):
#         self.name = name

#     def __repr__(self):
#         return "<Questionnaire (%d) %s>" % (self.id, self.name)

#     def to_json(self):
#         json = {
#             'id': self.id,
#             'name': self.name
#         }
#         return json

# class Question(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(120))
#     questionType = db.Column(db.String(120))
#     questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))
#     questionnaire = db.relationship("Questionnaire", backref=db.backref(
#         "questions", lazy="dynamic"))

#     __mapper_args__ = {
#         'polymorphic_identity': 'question',
#         'polymorphic_on': questionType
#     }

#     def __init__(self, title, questionType, questionnaire_id):
#         self.title = title
#         self.questionType = questionType
#         self.questionnaire_id = questionnaire_id

#     def to_json(self):
#         json = {
#             'id': self.id,
#             'title': self.title,
#             'questionType': self.questionType,
#             'questionnaire_id': self.questionnaire_id
#         }
#         return json

# class OpenQuestion(Question):
#     __mapper_args__ = {
#         'polymorphic_identity': 'open'
#     }

#     def __init__(self, title, questionnaire_id):
#         super().__init__(title, 'open', questionnaire_id)

# class MultipleChoiceQuestion(Question):
#     __mapper_args__ = {
#         'polymorphic_identity': 'multiple_choice'
#     }

#     def __init__(self, title, questionnaire_id, choices):
#         super().__init__(title, 'multiple_choice', questionnaire_id)
#         self.choices = choices

#     choices = db.Column(db.String(500))

#     def to_json(self):
#         json = super().to_json()
#         json['choices'] = self.choices
#         return json
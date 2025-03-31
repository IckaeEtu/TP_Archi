from flask import jsonify, abort, make_response, request, url_for
from .app import app, db
from .models import Questionnaire, Question
import json


def make_public_questionnaire(questionnaire):
    new_questionnaire = {}
    for field in ['id', 'name']:
        if field == 'id':
            new_questionnaire['uri'] = url_for('get_questionnaire', 
                                               questionnaire_id=questionnaire['id'], 
                                               _external=True)
        else:
            new_questionnaire[field] = questionnaire[field]
    return new_questionnaire


def make_public_question(question, questionnaire_id):
    new_question = {}
    for field in ['id', 'title', 'questionType', 'questionnaire_id']:
        if field == 'id':
            new_question['uri'] = url_for('get_question', question_id=question['id'], questionnaire_id=questionnaire_id, _external=True)
        else:
            new_question[field] = question[field]
    return new_question


@app.route('/quiz/api/v1.0/questionnaires', methods=['GET'])
def get_questionnaires():
    questionnaires = Questionnaire.query.all()
    return jsonify({'questionnaires': [make_public_questionnaire(q.to_json()) for q in questionnaires]})


@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>', methods=['GET'])
def get_questionnaire(questionnaire_id):
    questionnaire = Questionnaire.query.get(questionnaire_id)
    if not questionnaire:
        abort(404)
    
    return jsonify({'questionnaire': make_public_questionnaire(questionnaire.to_json())})


@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>/questions', methods=['GET'])
def get_questions(questionnaire_id):
    questionnaire = Questionnaire.query.get(questionnaire_id)
    if not questionnaire:
        abort(404)
    questions = Question.query.filter_by(questionnaire_id=questionnaire_id).all()
    return jsonify({'questions': [make_public_question(q.to_json(), questionnaire_id) for q in questions]})


@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>/question/<int:question_id>')
def get_question(question_id, questionnaire_id):
    question = Question.query.get(question_id)
    if not question:
        abort(404)

    return jsonify({'question': make_public_question(question.to_json(), questionnaire_id)})

@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>/question/<int:question_id>', methods=['DELETE'])
def delete_question(questionnaire_id, question_id):
    Question.query.filter_by(id=question_id).delete()
    db.session.commit()
    return jsonify(suppression=True)

@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>', methods=['DELETE'])
def delete_questionnaire(questionnaire_id):
    Questionnaire.query.filter_by(id=questionnaire_id).delete()

    db.session.commit()
    return jsonify(suppression=True)

@app.route('/quiz/api/v1.0/questionnaires', methods=['POST'])
def create_questionnaire() -> json:
    if not request.json or 'name' not in request.json:
        abort(400)

    questionnaire = Questionnaire(request.json['name'])
    db.session.add(questionnaire)
    db.session.commit()

    return jsonify({'questionnaire': make_public_questionnaire(questionnaire.to_json())}), 201

@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>', methods=['PUT'])
def modify_questionnaire(questionnaire_id):
    questionnaire = Questionnaire.query.get(questionnaire_id)
    if not questionnaire:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name'])!= str:
        abort(400)

    questionnaire.name = request.json.get('name', questionnaire.name)

    db.session.commit()
    return jsonify({'questionnaire': make_public_questionnaire(questionnaire.to_json())})

@app.route('/quiz/api/v1.0/questionnaires/<questionnaire_id>/questions', methods=['POST'])
def create_question(questionnaire_id) -> json:
    if not request.json or 'title' not in request.json or 'questionType' not in request.json:
        abort(400)

    question = Question(request.json['title'], request.json['questionType'], questionnaire_id)
    db.session.add(question)
    db.session.commit()

    return jsonify({'question': make_public_question(question.to_json(), questionnaire_id)}), 201

@app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>/question/<int:question_id>', methods=['PUT'])
def modify_question(questionnaire_id, question_id):
    question = Question.query.get(question_id)
    if not question:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title'])!= str:
        abort(400)
    if 'questionType' in request.json and type(request.json['questionType'])!= str:
        abort(400)

    question.title = request.json.get('title', question.title)
    question.questionType = request.json.get('questionType', question.questionType)

    db.session.commit()
    return jsonify({'question': make_public_question(question.to_json(), questionnaire_id)})


# from flask import jsonify, abort, make_response, request, url_for
# from .app import app, db
# from .models import Questionnaire, Question, OpenQuestion, MultipleChoiceQuestion
# import json

# def make_public_questionnaire(questionnaire):
#     new_questionnaire = {}
#     for field in ['id', 'name']:
#         if field == 'id':
#             new_questionnaire['uri'] = url_for('get_questionnaire', 
#                                                questionnaire_id=questionnaire['id'], 
#                                                _external=True)
#         else:
#             new_questionnaire[field] = questionnaire[field]
#     return new_questionnaire

# def make_public_question(question, questionnaire_id):
#     new_question = {}
#     for field in ['id', 'title', 'questionType', 'questionnaire_id']:
#         if field == 'id':
#             new_question['uri'] = url_for('get_question', question_id=question['id'], questionnaire_id=questionnaire_id, _external=True)
#         else:
#             new_question[field] = question[field]
#     if question['questionType'] == 'multiple_choice':
#         new_question['choices'] = question['choices']
#     return new_question

# @app.route('/quiz/api/v1.0/questionnaires', methods=['GET'])
# def get_questionnaires():
#     questionnaires = Questionnaire.query.all()
#     return jsonify({'questionnaires': [make_public_questionnaire(q.to_json()) for q in questionnaires]})

# @app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>', methods=['GET'])
# def get_questionnaire(questionnaire_id):
#     questionnaire = Questionnaire.query.get(questionnaire_id)
#     if not questionnaire:
#         abort(404)
    
#     return jsonify({'questionnaire': make_public_questionnaire(questionnaire.to_json())})

# @app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>/questions', methods=['GET'])
# def get_questions(questionnaire_id):
#     questionnaire = Questionnaire.query.get(questionnaire_id)
#     if not questionnaire:
#         abort(404)
#     questions = Question.query.filter_by(questionnaire_id=questionnaire_id).all()
#     return jsonify({'questions': [make_public_question(q.to_json(), questionnaire_id) for q in questions]})

# @app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>/question/<int:question_id>', methods=['GET'])
# def get_question(question_id, questionnaire_id):
#     question = Question.query.get(question_id)
#     if not question:
#         abort(404)

#     return jsonify({'question': make_public_question(question.to_json(), questionnaire_id)})

# @app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>/question/<int:question_id>', methods=['DELETE'])
# def delete_question(questionnaire_id, question_id):
#     Question.query.filter_by(id=question_id).delete()
#     db.session.commit()
#     return jsonify(suppression=True)

# @app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>', methods=['DELETE'])
# def delete_questionnaire(questionnaire_id):
#     Questionnaire.query.filter_by(id=questionnaire_id).delete()
#     db.session.commit()
#     return jsonify(suppression=True)

# @app.route('/quiz/api/v1.0/questionnaires', methods=['POST'])
# def create_questionnaire() -> json:
#     if not request.json or 'name' not in request.json:
#         abort(400)

#     questionnaire = Questionnaire(request.json['name'])
#     db.session.add(questionnaire)
#     db.session.commit()

#     return jsonify({'questionnaire': make_public_questionnaire(questionnaire.to_json())}), 201

# @app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>', methods=['PUT'])
# def modify_questionnaire(questionnaire_id):
#     questionnaire = Questionnaire.query.get(questionnaire_id)
#     if not questionnaire:
#         abort(404)
#     if not request.json:
#         abort(400)
#     if 'name' in request.json and type(request.json['name'])!= str:
#         abort(400)

#     questionnaire.name = request.json.get('name', questionnaire.name)

#     db.session.commit()
#     return jsonify({'questionnaire': make_public_questionnaire(questionnaire.to_json())})

# @app.route('/quiz/api/v1.0/questionnaires/<questionnaire_id>/questions', methods=['POST'])
# def create_question(questionnaire_id) -> json:
#     if not request.json or 'title' not in request.json or 'questionType' not in request.json:
#         abort(400)

#     questionType = request.json['questionType']
#     if questionType == 'open':
#         question = OpenQuestion(request.json['title'], questionnaire_id)
#     elif questionType == 'multiple_choice':
#         if 'choices' not in request.json:
#             abort(400)
#         question = MultipleChoiceQuestion(request.json['title'], questionnaire_id, request.json['choices'])
#     else:
#         abort(400)

#     db.session.add(question)
#     db.session.commit()

#     return jsonify({'question': make_public_question(question.to_json(), questionnaire_id)}), 201

# @app.route('/quiz/api/v1.0/questionnaires/<int:questionnaire_id>/question/<int:question_id>', methods=['PUT'])
# def modify_question(questionnaire_id, question_id):
#     question = Question.query.get(question_id)
#     if not question:
#         abort(404)
#     if not request.json:
#         abort(400)
#     if 'title' in request.json and type(request.json['title'])!= str:
#         abort(400)
#     if 'questionType' in request.json and type(request.json['questionType'])!= str:
#         abort(400)

#     question.title = request.json.get('title', question.title)
#     question.questionType = request.json.get('questionType', question.questionType)
#     if question.questionType == 'multiple_choice' and 'choices' in request.json:
#         question.choices = request.json['choices']

#     db.session.commit()
#     return jsonify({'question': make_public_question(question.to_json(), questionnaire_id)})
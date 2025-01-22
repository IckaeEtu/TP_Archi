from flask import jsonify, abort, make_response, request, url_for
from .app import app
from .models import tasks
import json


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task',
                                      task_id=task['id'],
                                      _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks=[make_public_task(t) for t in tasks])


@app.route('/todo/api/v1.0/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    for t in tasks:
        if t['id'] == task_id:
            t['uri'] = url_for('get_task', task_id=t['id'], _external=True)
            return t
    return None


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task() -> json:
    if not request.json or 'title' not in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': make_public_task(task)}), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

# curl -i http://localhost:5000/todo/api/v1.0/tasks test url avec get

# curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:5000/todo/api/v1.0/tasks
# h = permet de préciser le header
# -X POST -d '{"title":"Read a book"}' = précise ce qu'il y aura dans post
#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py
export FLASK_ENV=development
flask run &

# fais avec l'IA
HTML_FILE_PATH="$(pwd)/Questionnaire/todo-rest-client-promises/todo.html"
xdg-open "$HTML_FILE_PATH"
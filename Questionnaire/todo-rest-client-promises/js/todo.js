
$(function () {

    $("#button").click(refreshQuestionnairesList);

    function remplirQuestionnaires(data) {
        console.log(data);
        $('#questionnaires').empty();
        $('#questionnaires').append($('<ul>'));
        if (data && data.questionnaires) {
            for (const questionnaire of data.questionnaires) {
                console.log(questionnaire);
                $('#questionnaires ul')
                    .append($('<li>')
                        .append($('<a>')
                            .text(questionnaire.name)
                        ).on("click", questionnaire, details)
                    );
            }

        } else {
            $('#questionnaires ul').append($('<li>').text("No questionnaires found."));
        }
    }

    function remplirQuestions(data) {
        console.log(data);
        $('#questions').empty();
        $('#questions').append($('<ul>'));
        if (data && data.questions) {
            for (const question of data.questions) {
                console.log(question);
                $('#questions ul')
                    .append($('<li>')
                        .append($('<a>')
                            .text(question.title)
                        ).on("click", question, detailQuestion)
                    );
            }
        } else {
            $('#questions ul').append($('<li>').text("No questions found."));
        }
    }

    function onerror(err) {
        $("#questionnaires").html("<b>Impossible de récupérer les questionnaires !</b>" + err);
    }

    function refreshQuestionnairesList() {
        $("#currentquestionnaire").empty();
        requete = "http://127.0.0.1:5000/quiz/api/v1.0/questionnaires";
        fetch(requete)
            .then(response => {
                if (response.ok) return response.json();
                else throw new Error('Problème ajax: ' + response.status);
            }
            )
            .then(remplirQuestionnaires)
            .catch(onerror);
    }

    function refreshQuestionsList(questionnaire) {
        console.log(questionnaire);
        $("#currentquestion").empty();
        requete = questionnaire.uri + "/questions";
        fetch(requete)
            .then(response => {
                if (response.ok) return response.json();
                else throw new Error('Problème ajax: ' + response.status);
            }
            )
            .then(remplirQuestions)
            .catch(onerror);
    }

    function details(event) {
        $("#currentquestionnaire").empty();
        questionnaire = event.data;
        formTask();
        fillFormTask(questionnaire);
        refreshQuestionsList(questionnaire);
    }

    function detailQuestion(event) {
        const question = event.data;
        $("#currentquestion").empty();
        console.log(question);
        formQuestion();
        fillFormQuestion(question);
    }

    $("#tools #add").on("click", formTask);
    $('#tools #del').on('click', delTask);

    $('#tools #add_question').on('click', formQuestion);
    $('#tools #del_question').on('click', delQuestion);

    function formTask(isnew) {
        $("#currentquestionnaire").empty();
        $("#currentquestionnaire")
            .append($('<span>name<input type="text" id="name"><br></span>'))
            .append($('<span><input type="hidden" id="turi"><br></span>'))
            .append(isnew ? $('<span><input type="button" value="Save Task"><br></span>').on("click", saveNewTask)
                : $('<span><input type="button" value="Modify Task"><br></span>').on("click", saveModifiedQuestionnaire)
            );
    }

    function formQuestion(isnew) {
        $("#currentquestion").empty();
        $("#currentquestion")
            .append($('<span>title<input type="text" id="title"><br></span>'))
            .append($('<span>type<input type="text" id="type"><br></span>'))
            .append($('<span><input type="hidden" id="turi"><br></span>'))
            .append(isnew ? $('<span><input type="button" value="Save Question"><br></span>').on("click", saveNewQuestion)
                : $('<span><input type="button" value="Modify Question"><br></span>').on("click", saveModifiedQuestion)
            );
    }

    function fillFormTask(t) {
        $("#currentquestionnaire #name").val(t.name);
        t.uri = (t.uri == undefined) ? "http://127.0.0.1:5000/quiz/api/v1.0/questionnaire" + t.id : t.uri;
        $("#currentquestionnaire #turi").val(t.uri);
    }

    function fillFormQuestion(t) {
        console.log( $("#currentquestion #title"));
        $("#currentquestion #title").val(t.title);
        $("#currentquestion #type").val(t.questionType);
        t.uri = (t.uri == undefined) ? "http://127.0.0.1:5000/quiz/api/v1.0/question/" + t.id : t.uri;
        $("#currentquestion #turi").val(t.uri);
    }

    class Questionnaire {
        constructor(name) {
            this.name = name;
        }
    }

    class Question {
        constructor(title, type) {
            this.title = title;
            this.questionType = type;
        }
    }

    function saveNewTask() {
        var name = $("#currentquestionnaire #name").val();
        questionnaire = new Questionnaire(name);

        fetch("http://127.0.0.1:5000/quiz/api/v1.0/questionnaires", {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify(questionnaire)
        })
            .then(res => {
                console.log('Save Success');
                console.log(res)
                $("#result").text(res['contenu']);
                refreshQuestionnairesList();
            })
            .catch(res => { console.log(res) });
    }

    function saveModifiedQuestionnaire() {
        const questionnaireName = $('#currentquestionnaire #name').val();
        const questionnaire = new Questionnaire(questionnaireName);
        const questionnaireUri = $('#currentquestionnaire #turi').val();

        console.log("PUT");
        console.log(questionnaireUri);
        console.log(JSON.stringify(questionnaire));

        fetch(questionnaireUri, {
            method: "PUT",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(questionnaire)
        })
            .then(response => {
                if (response.ok) {
                    console.log('Update Success');
                    refreshQuestionnairesList();
                } else {
                    console.error('Error updating questionnaire:', response.status);
                }
            })
            .catch(error => {
                console.error('Error updating questionnaire:', error);
            });
    }
    function saveModifiedQuestion() {
        const questionTitle = $('#currentquestion #title').val();
        const questionType = $('#currentquestion #type').val();
        const questionUri = $('#currentquestion #turi').val();
        const question = new Question(questionTitle, questionType);
        
        console.log("Question data:", question);
    
        fetch(questionUri, {
            method: "PUT",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(question) 
        })
        .then(response => {
            if (response.ok) {
                console.log('Update Success');
                refreshQuestionsList({ uri: questionUri.split('/question/')[0] });
            } else {
                console.error('Error updating question:', response.status);
            }
        })
        .catch(error => {
            console.error('Error updating question:', error);
        });
    }

    function saveNewQuestion() {
        var title = $("#currentquestion #title").val();
        var type = $("#currentquestion #type").val();
        var questionnaireUri = $("#currentquestionnaire #turi").val();
        var questionnaireId = $("#currentquestionnaire #turi").val().split('/').pop();
        var question = new Question(title, type);

        console.log(questionnaireUri+"/questions");
        console.log(JSON.stringify(question));

        fetch(questionnaireUri + "/questions", {
            headers: {
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify(question)
        })
            .then(res => {
                console.log('Save Success');
                console.log(res)
                $("#result").text(res['contenu']);
                refreshQuestionsList({ id: questionnaireId });
            })
            .catch(res => { console.log(res) });
    }

    function delTask() {
        if ($("#currentquestionnaire #turi").val()) {
            url = $("#currentquestionnaire #turi").val();
            fetch(url, {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                method: "DELETE"
            })
                .then(res => { console.log('Delete Success:' + res); })
                .then(refreshQuestionnairesList)
                .catch(res => { console.log(res); });
        }
    }

    function delQuestion() {
        if ($("#currentquestion #turi").val()) {
            url = $("#currentquestion #turi").val();
            fetch(url, {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                method: "DELETE"
            })
                .then(res => { console.log('Delete Success:' + res); })
                .then(refreshQuestionsList)
                .catch(res => { console.log(res); });
        }
    }
}); 

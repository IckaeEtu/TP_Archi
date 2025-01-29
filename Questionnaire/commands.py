import click
from flask.cli import with_appcontext

from .app import app, db
from .models import Questionnaire, Question

@app.cli.command("sync_db")
def sync_db():

    with app.app_context():
        db.drop_all()
        db.create_all()
    # Création de questionnaires
        questionnaire1 = Questionnaire(name="Satisfaction client")
        questionnaire2 = Questionnaire(name="Évaluation des employés")
        questionnaire3 = Questionnaire(name="Sondage sur le produit")

        db.session.add_all([questionnaire1, questionnaire2, questionnaire3])
        db.session.commit()

        # Création de questions pour "Satisfaction client"
        questions_satisfaction = [
            Question(title="Êtes-vous satisfait de nos produits ?", questionType="Choix multiple", questionnaire_id=questionnaire1.id),
            Question(title="Comment évalueriez-vous notre service client ?", questionType="Échelle", questionnaire_id=questionnaire1.id),
            Question(title="Recommanderiez-vous notre entreprise à un ami ?", questionType="Oui/Non", questionnaire_id=questionnaire1.id),
            Question(title="Avez-vous des suggestions d'amélioration ?", questionType="Texte", questionnaire_id=questionnaire1.id)
        ]

        # Création de questions pour "Évaluation des employés"
        questions_employes = [
            Question(title="Comment évalueriez-vous votre satisfaction au travail ?", questionType="Échelle", questionnaire_id=questionnaire2.id),
            Question(title="Vous sentez-vous soutenu par votre équipe ?", questionType="Oui/Non", questionnaire_id=questionnaire2.id),
            Question(title="Avez-vous les ressources nécessaires pour effectuer votre travail efficacement ?", questionType="Choix multiple", questionnaire_id=questionnaire2.id),
            Question(title="Avez-vous des commentaires ou suggestions ?", questionType="Texte", questionnaire_id=questionnaire2.id)
        ]

        # Création de questions pour "Sondage sur le produit"
        questions_produit = [
            Question(title="Comment avez-vous connu ce produit ?", questionType="Choix multiple", questionnaire_id=questionnaire3.id),
            Question(title="Quelle est la fréquence d'utilisation de ce produit ?", questionType="Échelle", questionnaire_id=questionnaire3.id),
            Question(title="Quelles sont les fonctionnalités que vous appréciez le plus ?", questionType="Texte", questionnaire_id=questionnaire3.id),
            Question(title="Recommanderiez-vous ce produit à d'autres ?", questionType="Oui/Non", questionnaire_id=questionnaire3.id)
        ]

        db.session.add_all(questions_satisfaction + questions_employes + questions_produit)
        db.session.commit()
        click.echo('Base de données synchronisée.')
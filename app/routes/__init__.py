from bson import ObjectId
from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from app.controllers import sondage_controller, reponse_controller
from app.controllers.sondage_controller import get_sondage_by_id
from app.models import get_sondage_collection, get_reponse_collection

# Fonction pour enregistrer les routes dans l'application Flask
def register_routes(app):
    # Route pour créer un sondage (GET : afficher le formulaire, POST : soumettre les données)
    @app.route('/create_sondage', methods=['GET', 'POST'])
    def create_sondage():
        if request.method == 'POST':
            # Récupération des données du formulaire
            data = request.form.to_dict()
            questions = []

            # Identifier les indices des questions dans les données du formulaire
            question_indices = set()
            for key in data.keys():
                if key.startswith('questions-') and '-intitule' in key:
                    question_indices.add(key.split('-')[1])  # Extraire l'indice unique

            # Construction de la liste des questions à partir des données récupérées
            for index in question_indices:
                question_data = {
                    "intitule": data.get(f'questions-{index}-intitule', ''),  # Titre de la question
                    "type": data.get(f'questions-{index}-type', ''),  # Type de question (texte ou QCM)
                    "reponses": []  # Liste des réponses pour les QCM
                }

                # Récupération des réponses associées à cette question
                reponse_keys = [key for key in data.keys() if key.startswith(f'questions-{index}-reponses-')]
                for reponse_key in sorted(reponse_keys):  # Tri pour conserver l'ordre
                    question_data["reponses"].append(data[reponse_key])

                # Ajout de la question à la liste des questions
                questions.append(question_data)

            # Création du dictionnaire du sondage à insérer dans la base de données
            sondage_data = {
                "nom": data.get('nom', ''),  # Nom du sondage
                "createur": data.get('createur', ''),  # Créateur du sondage
                "questions": questions  # Liste des questions
            }

            # Insertion du sondage dans la collection MongoDB
            collection = get_sondage_collection()
            collection.insert_one(sondage_data)

            # Redirection vers la page d'accueil après la création
            return redirect(url_for('index'))

        # Affichage du formulaire de création de sondage
        return render_template('create_sondage.html')

    # Route pour récupérer tous les sondages (appelant un contrôleur)
    @app.route('/sondages', methods=['GET'])
    def get_sondages():
        return sondage_controller.get_all_sondages()

    # Route pour la page d'accueil (liste des sondages)
    @app.route('/')
    def index():
        return sondage_controller.index()

    # Route pour soumettre une réponse à un sondage
    @app.route('/sondages/<sondage_id>/reponses', methods=['POST'])
    def submit_response_route(sondage_id):
        return reponse_controller.submit_response(sondage_id)

    # Route pour afficher le détail d'un sondage
    @app.route('/sondages/<sondage_id>', methods=['GET'])
    def show_sondage(sondage_id):
        try:
            # Conversion de l'ID en ObjectId (MongoDB)
            sondage_id = ObjectId(sondage_id)
        except Exception as e:
            return "ID invalide", 400  # Erreur si l'ID n'est pas valide

        # Récupération du sondage dans la collection MongoDB
        collection = get_sondage_collection()
        sondage = collection.find_one({"_id": sondage_id})

        if sondage:
            # Affichage de la page de détail du sondage
            return render_template('sondage_detail.html', sondage=sondage)
        else:
            # Retourne une erreur si le sondage n'est pas trouvé
            return "Sondage non trouvé", 404

from flask import request, jsonify, session
from bson import ObjectId
from app.models import get_reponse_collection

def submit_response(sondage_id):
    # Tentative de conversion de l'ID du sondage en ObjectId (format MongoDB)
    try:
        sondage_id = ObjectId(sondage_id)
    except Exception as e:
        # Retourne une erreur si l'ID fourni est invalide
        return jsonify({"message": "ID de sondage invalide."}), 400

    # Récupération des réponses envoyées dans la requête sous forme de liste
    reponses = {}
    for question in request.form:
        # On récupère les réponses pour chaque question
        reponses[question] = request.form.getlist(question)

    # Vérifie si aucune réponse n'a été envoyée
    if not reponses:
        return jsonify({"message": "Aucune réponse envoyée."}), 400

    utilisateur_id = session.get('username')  # Assurez-vous que 'username' est stocké dans la session lors de la connexion

    # Préparation des données à enregistrer
    data = {
        "sondage_id": sondage_id,  # Référence au sondage concerné
        "utilisateur_id": utilisateur_id,  # Identifiant d'utilisateur (peut être remplacé par un système d'authentification)
        "reponses": reponses  # Dictionnaire des réponses pour chaque question
    }

    # Tentative d'insertion des réponses dans la base de données
    try:
        # Récupération de la collection MongoDB pour les réponses
        collection = get_reponse_collection()
        collection.insert_one(data)
    except Exception as e:
        # Retourne une erreur si un problème survient lors de l'insertion
        return jsonify({"message": "Erreur lors de l'enregistrement des réponses."}), 500

    # Retourne un message de succès si tout s'est bien passé
    return jsonify({"message": "Réponse enregistrée avec succès !"}), 201

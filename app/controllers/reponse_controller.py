from flask import request, jsonify
from bson import ObjectId
from app.models import get_reponse_collection

# Fonction pour soumettre une réponse à un sondage
def submit_response(sondage_id):
    # Tentative de conversion de l'ID du sondage en ObjectId (format MongoDB)
    try:
        sondage_id = ObjectId(sondage_id)
    except Exception as e:
        # Retourne une erreur si l'ID fourni est invalide
        return jsonify({"message": "ID de sondage invalide."}), 400

    # Récupération des réponses envoyées dans la requête sous forme de liste
    reponses = request.form.getlist('reponses[]')

    # Vérifie si aucune réponse n'a été envoyée
    if not reponses:
        return jsonify({"message": "Aucune réponse envoyée."}), 400

    # Préparation des données à enregistrer
    data = {
        "sondage_id": sondage_id,  # Référence au sondage concerné
        "utilisateur_id": "utilisateur1",  # Identifiant d'utilisateur (peut être remplacé par un système d'authentification)
        "reponses": reponses  # Liste des réponses fournies
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

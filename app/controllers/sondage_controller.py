from bson import ObjectId
from flask import render_template, request, jsonify
from app.models import get_sondage_collection


# Fonction pour créer un sondage
def create_sondage():
    # Récupération des données envoyées via la requête JSON
    data = request.json

    # Récupération de la collection MongoDB pour stocker les sondages
    collection = get_sondage_collection()

    # Insertion des données dans la collection
    collection.insert_one(data)

    # Retourne une réponse JSON indiquant que le sondage a été créé
    return jsonify({"message": "Sondage créé avec succès !"}), 201


# Fonction pour récupérer tous les sondages
def get_all_sondages():
    # Récupération de la collection MongoDB contenant les sondages
    collection = get_sondage_collection()

    # Requête pour obtenir tous les sondages, en excluant le champ "_id"
    sondages = list(collection.find({}, {"_id": 0}))

    # Si aucun sondage n'est trouvé, renvoyer un message approprié
    if not sondages:
        return jsonify({"message": "Aucun sondage trouvé."}), 404

    # Retourne une réponse JSON contenant la liste des sondages
    return jsonify(sondages), 200


from flask import render_template
from app.models import get_sondage_collection


# Fonction pour afficher la page d'accueil contenant la liste des sondages
def index():
    # Récupération de la collection MongoDB
    collection = get_sondage_collection()

    # Vérification si la collection existe
    if collection is None:
        return jsonify({"message": "Erreur : la collection 'sondages' n'a pas été trouvée."}), 500

    # Requête pour récupérer les sondages avec seulement les champs nécessaires
    sondages = list(collection.find({}, {"_id": 1, "nom": 1, "createur": 1}))

    # Conversion des IDs MongoDB en chaînes de caractères pour éviter les problèmes d'affichage
    for sondage in sondages:
        sondage['id_str'] = str(sondage['_id'])

    # Si aucun sondage n'est trouvé, retourne un message approprié
    if not sondages:
        return jsonify({"message": "Aucun sondage trouvé."}), 404

    # Retourne le rendu du template HTML avec la liste des sondages
    return render_template('index.html', sondages=sondages)


# Fonction pour récupérer un sondage spécifique par son ID
def get_sondage_by_id(sondage_id):
    try:
        # Conversion de l'ID reçu en ObjectId (format utilisé par MongoDB)
        sondage_id = ObjectId(sondage_id)
    except Exception as e:
        # Retourne une erreur si l'ID est invalide
        return "ID invalide", 400

    # Récupération de la collection MongoDB
    collection = get_sondage_collection()

    # Recherche du sondage correspondant à l'ID, en excluant le champ "_id"
    sondage = collection.find_one({"_id": sondage_id}, {"_id": 0})

    # Si le sondage est trouvé, retourne le template HTML avec les détails du sondage
    if sondage:
        return render_template('sondage_detail.html', sondage=sondage)
    else:
        # Retourne une erreur si le sondage n'est pas trouvé
        return "Sondage non trouvé", 404

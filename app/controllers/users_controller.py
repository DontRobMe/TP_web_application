from flask import request, jsonify, session
from werkzeug.security import generate_password_hash
from bson import ObjectId
from app.models import get_user_collection  # Assurez-vous que cette fonction retourne votre collection MongoDB pour les utilisateurs

from werkzeug.security import generate_password_hash
from flask import request, jsonify
from app.models import get_user_collection

def register_user():
    try:
        # Assurez-vous que les champs existent dans la requête
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Vérification si les champs sont bien remplis
        if not all([username, email, password, confirm_password]):
            return jsonify({"message": "Tous les champs sont obligatoires."}), 400

        # Vérification que les mots de passe correspondent
        if password != confirm_password:
            return jsonify({"message": "Les mots de passe ne correspondent pas."}), 400

        # Hachage du mot de passe
        hashed_password = generate_password_hash(password)

        # Vérification si l'utilisateur existe déjà
        collection = get_user_collection()
        existing_user = collection.find_one({"username": username})

        if existing_user:
            return jsonify({"message": "Nom d'utilisateur déjà pris."}), 400

        # Insertion de l'utilisateur dans la base de données
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password
        }
        collection.insert_one(user_data)

        return jsonify({"message": "Inscription réussie."}), 201

    except Exception as e:
        # Capture de toute exception et retour d'un message d'erreur
        return jsonify({"message": f"Erreur lors de l'inscription: {str(e)}"}), 500



def get_user_by_id(user_id):
    try:
        # Vérification si l'ID de l'utilisateur est valide
        try:
            user_id = ObjectId(user_id)
        except Exception:
            return jsonify({"message": "ID utilisateur invalide."}), 400

        # Récupération de l'utilisateur
        collection = get_user_collection()
        user = collection.find_one({"_id": user_id})

        if not user:
            return jsonify({"message": "Utilisateur non trouvé."}), 404

        # Exclure le mot de passe pour la réponse
        user_data = {
            "username": user["username"],
            "email": user["email"]
        }

        return jsonify({"user": user_data}), 200

    except Exception as e:
        return jsonify({"message": f"Erreur lors de la récupération de l'utilisateur: {str(e)}"}), 500



def update_user(user_id):
    try:
        # Vérification de l'ID de l'utilisateur
        try:
            user_id = ObjectId(user_id)
        except Exception:
            return jsonify({"message": "ID utilisateur invalide."}), 400

        # Récupération des données du formulaire
        new_email = request.form.get('email', None)
        new_password = request.form.get('password', None)
        hashed_password = None

        if new_password:
            # Hacher le nouveau mot de passe si fourni
            hashed_password = generate_password_hash(new_password)

        # Préparation de la mise à jour
        update_data = {}
        if new_email:
            update_data['email'] = new_email
        if hashed_password:
            update_data['password'] = hashed_password

        # Mise à jour des informations de l'utilisateur dans la base de données
        collection = get_user_collection()
        result = collection.update_one({"_id": user_id}, {"$set": update_data})

        if result.matched_count == 0:
            return jsonify({"message": "Utilisateur non trouvé."}), 404

        return jsonify({"message": "Utilisateur mis à jour avec succès."}), 200

    except Exception as e:
        return jsonify({"message": f"Erreur lors de la mise à jour de l'utilisateur: {str(e)}"}), 500



def delete_user(user_id):
    try:
        try:
            user_id = ObjectId(user_id)
        except Exception:
            return jsonify({"message": "ID utilisateur invalide."}), 400

        collection = get_user_collection()
        result = collection.delete_one({"_id": user_id})

        if result.deleted_count == 0:
            return jsonify({"message": "Utilisateur non trouvé."}), 404

        return jsonify({"message": "Utilisateur supprimé avec succès."}), 200

    except Exception as e:
        return jsonify({"message": f"Erreur lors de la suppression de l'utilisateur: {str(e)}"}), 500

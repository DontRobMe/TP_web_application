from flask import request, jsonify, session
from bson import ObjectId
from app.controllers import sondage_controller, reponse_controller
from app.models import get_sondage_collection, get_reponse_collection, get_user_collection
from werkzeug.security import generate_password_hash, check_password_hash


# Fonction pour enregistrer les routes dans l'application Flask
def register_routes(app):
    # Route pour la page d'accueil avec contrôle d'authentification
    # Route pour la page d'accueil avec contrôle d'authentification
    from flask import request

    @app.route('/', methods=['GET'])
    def index():
        if 'username' not in session:
            flash("Veuillez vous connecter pour accéder à la page principale.", "warning")
            return redirect(url_for('login'))

        # Récupérer le filtre sélectionné et l'utilisateur choisi
        filter_choice = request.args.get('filter', 'all')  # Par défaut 'all' si aucun filtre
        selected_user = filter_choice if filter_choice != 'all' else ''  # Si un utilisateur est choisi, sinon empty

        # Récupérer la liste des utilisateurs pour le formulaire
        collection = get_sondage_collection()
        users_collection = get_user_collection()  # Liste des utilisateurs
        users = [user['username'] for user in users_collection.find()]  # Liste des utilisateurs

        # Filtrer les sondages en fonction du filtre choisi
        if selected_user:
            sondages = collection.find({'createur': selected_user})  # Filtrer par l'utilisateur sélectionné
        else:
            sondages = collection.find()  # Afficher tous les sondages

        # Convertir les sondages en liste
        sondages_list = list(sondages)

        return render_template('index.html', username=session['username'], sondages=sondages_list, filter=filter_choice,
                               users=users, selected_user=selected_user)

    # Route pour créer un sondage (GET pour afficher le formulaire, POST pour soumettre)
    from flask import render_template, request, session, redirect, url_for, flash
    from app.models import get_sondage_collection

    @app.route('/create_sondage', methods=['GET', 'POST'])
    def create_sondage():
        # Vérifie si l'utilisateur est connecté
        if 'username' not in session:
            flash("Veuillez vous connecter avant de créer un sondage.", "warning")
            return redirect(url_for('login'))  # Redirige vers la page de connexion si non connecté

        if request.method == 'POST':
            data = request.form.to_dict()
            questions = []

            # Construction de la liste des questions à partir des données
            question_indices = {key.split('-')[1] for key in data.keys() if
                                key.startswith('questions-') and '-intitule' in key}
            for index in question_indices:
                question_data = {
                    "intitule": data.get(f'questions-{index}-intitule', ''),
                    "type": data.get(f'questions-{index}-type', ''),
                    "reponses": [data[reponse_key] for reponse_key in sorted(data.keys()) if
                                 reponse_key.startswith(f'questions-{index}-reponses-')]
                }
                questions.append(question_data)

            # Ajoute le créateur dans les données du sondage
            sondage_data = {
                "nom": data.get('nom', ''),
                "createur": session['username'],  # Utilisation du nom de l'utilisateur dans la session
                "questions": questions
            }

            # Insertion dans la base de données MongoDB
            collection = get_sondage_collection()
            collection.insert_one(sondage_data)

            flash("Sondage créé avec succès !", "success")
            return redirect(url_for('index'))  # Redirige vers la page d'accueil après la création

        return render_template('create_sondage.html')

    # Route pour afficher un sondage spécifique
    @app.route('/sondages/<sondage_id>', methods=['GET'])
    def show_sondage(sondage_id):
        try:
            sondage_id = ObjectId(sondage_id)
        except Exception:
            return "ID invalide", 400

        collection = get_sondage_collection()
        sondage = collection.find_one({"_id": sondage_id})

        if sondage:
            return render_template('sondage_detail.html', sondage=sondage)
        else:
            return "Sondage non trouvé", 404

    @app.route('/sondages/<sondage_id>/reponses', methods=['POST'])
    def submit_response_route(sondage_id):
        if 'username' not in session:
            flash("Veuillez vous connecter pour soumettre une réponse.", "warning")
            return redirect(url_for('login'))

        return reponse_controller.submit_response(sondage_id)

    # Page de succès après une soumission
    @app.route('/success', methods=['GET'])
    def success_page():
        return render_template('success_page.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if password != confirm_password:
                flash("Les mots de passe ne correspondent pas.", "danger")
                return redirect(url_for('register'))

            hashed_password = generate_password_hash(password)

            collection = get_user_collection()
            existing_user = collection.find_one({"username": username})
            existing_email = collection.find_one({"email": email})

            if existing_user:
                flash("Ce nom d'utilisateur est déjà pris.", "danger")
                return redirect(url_for('register'))

            if existing_email:
                flash("Cet email est déjà utilisé.", "danger")
                return redirect(url_for('register'))

            collection.insert_one({"username": username, "email": email, "password": hashed_password})

            session['username'] = username
            flash("Inscription réussie ! Vous êtes maintenant connecté.", "success")
            return redirect(url_for('index'))

        return render_template('sub_page.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            collection = get_user_collection()
            user = collection.find_one({"username": username})

            if user and check_password_hash(user['password'], password):
                session['username'] = user['username']
                flash("Connexion réussie !", "success")
                return redirect(url_for('index'))
            else:
                flash("Nom d'utilisateur ou mot de passe incorrect.", "danger")
                return redirect(url_for('login'))

        return render_template('auth_page.html')

    @app.route('/logout')
    def logout():
        session.pop('username', None)
        flash("Déconnexion réussie.", "success")
        return redirect(url_for('index'))

    @app.route('/delete_sondage/<sondage_id>', methods=['POST'])
    def delete_sondage(sondage_id):
        if 'username' not in session:
            flash("Veuillez vous connecter pour supprimer un sondage.", "warning")
            return redirect(url_for('login'))

        try:
            # Convertir l'ID du sondage en ObjectId
            sondage_id = ObjectId(sondage_id)

            # Supprimer le sondage de la collection "sondages"
            sondage_collection = get_sondage_collection()
            sondage_collection.delete_one({"_id": sondage_id})

            # Supprimer les réponses associées à ce sondage de la collection "reponses"
            reponse_collection = get_reponse_collection()
            reponse_collection.delete_many({"sondage_id": sondage_id})

            return jsonify({"success": True, "message": "Sondage et réponses supprimés avec succès!"}), 200
        except Exception as e:
            return jsonify({"success": False, "message": f"Erreur lors de la suppression : {str(e)}"}), 500

    from flask import Flask, render_template, redirect, url_for, flash, session
    from bson import ObjectId
    from collections import Counter

    @app.route('/view_reponses/<sondage_id>', methods=['GET'])
    def view_reponses(sondage_id):
        if 'username' not in session:
            flash("Veuillez vous connecter pour accéder aux réponses.", "warning")
            return redirect(url_for('login'))

        # Récupérer le sondage
        collection = get_sondage_collection()
        sondage = collection.find_one({'_id': ObjectId(sondage_id)})

        if not sondage:
            flash("Sondage introuvable.", "danger")
            return redirect(url_for('index'))

        # Récupérer les réponses
        reponses_collection = get_reponse_collection()
        reponses = reponses_collection.find({'sondage_id': ObjectId(sondage_id)})
        reponses_list = list(reponses)

        # **Générer les données pour le graphique**
        reponse_counts = {}  # Dictionnaire pour compter les réponses
        for reponse in reponses_list:
            for rep in reponse.get("reponses", {}).get("reponses_", []):  # Accéder à la liste des réponses
                reponse_counts[rep] = reponse_counts.get(rep, 0) + 1  # Compter les réponses

        labels = list(reponse_counts.keys())  # Labels = Réponses uniques
        data_values = list(reponse_counts.values())  # Valeurs = Nombre de votes par réponse

        return render_template(
            'view_reponses.html',
            sondage=sondage,
            reponses=reponses_list,
            labels=labels,
            data_values=data_values
        )

    from flask import Flask, render_template, request, redirect, url_for, flash, session
    from bson import ObjectId

    @app.route('/edit_sondage/<sondage_id>', methods=['GET', 'POST'])
    def edit_sondage(sondage_id):
        # Vérifier que l'utilisateur est connecté
        if 'username' not in session:
            flash("Veuillez vous connecter pour éditer un sondage.", "warning")
            return redirect(url_for('login'))

        # Récupérer le sondage depuis la base de données
        collection = get_sondage_collection()
        sondage = collection.find_one({'_id': ObjectId(sondage_id)})

        if not sondage:
            flash("Sondage introuvable.", "danger")
            return redirect(url_for('index'))

        # Vérifier que l'utilisateur connecté est bien le créateur du sondage
        if sondage.get('createur') != session['username']:
            flash("Vous n'êtes pas autorisé à éditer ce sondage.", "danger")
            return redirect(url_for('index'))

        if request.method == 'POST':
            # Récupérer les données du formulaire (ici, on met à jour le nom du sondage)
            nom = request.form.get('nom')
            # Vous pouvez ajouter ici la mise à jour des questions/options si nécessaire

            # Mettre à jour le sondage dans la base de données
            collection.update_one({'_id': ObjectId(sondage_id)}, {"$set": {"nom": nom}})
            flash("Sondage mis à jour avec succès.", "success")
            return redirect(url_for('index'))

        # Pour la méthode GET, afficher le formulaire pré-rempli avec les données du sondage
        return render_template('edit_sondage.html', sondage=sondage)

    @app.route('/update_sondage/<sondage_id>', methods=['POST'])
    def update_sondage(sondage_id):
        if 'username' not in session:
            flash("Veuillez vous connecter pour modifier un sondage.", "warning")
            return redirect(url_for('login'))

        collection = get_sondage_collection()
        sondage = collection.find_one({'_id': ObjectId(sondage_id)})

        if not sondage:
            flash("Sondage introuvable.", "danger")
            return redirect(url_for('index'))

        if sondage.get('createur') != session['username']:
            flash("Vous n'êtes pas autorisé à modifier ce sondage.", "danger")
            return redirect(url_for('index'))

        # Récupération des nouvelles données du formulaire
        nom = request.form.get('nom', sondage['nom'])

        questions = []
        question_indices = {key.split('-')[1] for key in request.form.keys() if key.startswith('questions-')}
        for index in question_indices:
            question_data = {
                "intitule": request.form.get(f'questions-{index}-intitule', ''),
                "type": request.form.get(f'questions-{index}-type', ''),
                "reponses": [request.form[reponse_key] for reponse_key in sorted(request.form.keys()) if
                             reponse_key.startswith(f'questions-{index}-reponses-')]
            }
            questions.append(question_data)

        # Mise à jour du sondage dans la base de données
        collection.update_one(
            {'_id': ObjectId(sondage_id)},
            {"$set": {"nom": nom, "questions": questions}}
        )

        flash("Sondage mis à jour avec succès.", "success")
        return redirect(url_for('index'))

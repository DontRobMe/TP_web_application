# 🗳️ Système de Sondage avec Flask et MongoDB

## 📖 Description

Ce projet est une application de système de sondage développée avec **Python** et le framework **Flask**, utilisant **MongoDB** comme base de données. 

### Fonctionnalités

#### 👥 Utilisateur Créateur
- **Créer un sondage** avec des questions ouvertes ou à choix multiples.
- **Modifier** les sondages et leurs questions associées.
- **Supprimer** un sondage.
- **Voir les résultats** des sondages que vous avez créés.

#### 📝 Utilisateur Répondant
- **Répondre à des sondages** publiés.
- Voir la liste des sondages disponibles.

#### 🔒 Authentification
- **Inscription** et **Connexion** des utilisateurs.
- **Déconnexion** de l'utilisateur.


---

## ⚙️ Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :

- ✅ Python 3.7 ou version supérieure
- ✅ MongoDB Community Edition (ou une instance MongoDB Cloud)
- ✅ pip (gestionnaire de paquets Python)

---

## 🚀 Installation

1. **Clonez le projet** :
   ```bash
   git clone https://github.com/votre-repo/sondage-app.git
   cd sondage-app

2. **Installez les dépendances Python** :

    ```bash
    pip install -r requirements.txt
   
3. **Démarrez MongoDB** :
    - Créez un dossier pour les données MongoDB si nécessaire :
      ```bash
      mkdir -p ./data/db
      
    - Démarrez le serveur MongoDB :
      ```bash
      mongod --dbpath=./data/db

4. **Démarrez l'application Flask** :

    ```bash
    python app.py

5. L'application sera accessible à l'adresse suivante : **http://localhost:5000**.


## 📚 Documentation des endpoints API

**Gestion des Sondages**

➕ Créer un sondage
    
- Endpoint : POST /sondages

📜 Obtenir la liste des sondages

- Endpoint : GET /sondages

✍️ Répondre à un sondage

- Endpoint : POST /reponses

**Gestion des utilisateurs**

🔒 Inscription

- Endpoint : POST /register

🔑 Connexion

- Endpoint : POST /login

🚪 Déconnexion

- Endpoint : GET /logout

**Gestion des sondages spécifiques**

👁 Voir les détails d'un sondage

- Endpoint : GET /sondages/<sondage_id>

📝 Éditer un sondage

- Endpoint : GET /edit_sondage/<sondage_id>

✏️ Mettre à jour un sondage

- Endpoint : POST /update_sondage/<sondage_id>

🗑 Supprimer un sondage

- Endpoint : POST /delete_sondage/<sondage_id>

📊 Voir les réponses d'un sondage

- Endpoint : GET /view_reponses/<sondage_id>

## 🛠️ Structure du Projet
```bash    
sondage-app/
├── app/
│   ├── __init__.py         
│   ├── models.py           
│   ├── routes.py           
│   ├── controllers/        
│   │   ├── sondage_controller.py
│   │   └── reponse_controller.py
│   │   └── users_controller.py
│   ├── services/           
│       ├── database.py
│   ├── templates/           
├── app.py                   
├── config.py                
├── requirements.txt         
└── README.md                
```


## 🔧 Configuration

**Pour configurer la connexion à MongoDB, modifiez le fichier config.py :**

```python
    class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/mydb")
```

## ✨ Auteur

- Nom : **DontRobMe**
- GitHub : **https://github.com/DontRobMe**
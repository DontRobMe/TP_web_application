# 🗳️ Système de Sondage avec Flask et MongoDB

## 📖 Description

Ce projet est une application de système de sondage développée avec **Python** et le framework **Flask**, utilisant **MongoDB** comme base de données. 

### Fonctionnalités

#### 👥 Utilisateur Créateur
- **Créer un sondage** avec des questions ouvertes ou à choix multiples.
- **Modifier** les sondages et leurs questions associées.
- **Supprimer** un sondage.

#### 📝 Utilisateur Répondant
- **Répondre à des sondages** publiés.
- Voir la liste des sondages disponibles.

#### 🌍 Public
- **Consulter la liste des sondages disponibles.**

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


## 🛠️ Structure du Projet
```bash    
sondage-app/
├── app/
│   ├── __init__.py          # Initialisation de l'application Flask
│   ├── models.py            # Modèles pour les collections MongoDB
│   ├── routes.py            # Gestion des routes de l'application
│   ├── controllers/         # Contrôleurs pour les fonctionnalités
│   │   ├── sondage_controller.py
│   │   └── reponse_controller.py
│   ├── services/            # Services pour la base de données et l'authentification
│       ├── database.py
│       └── auth_service.py
├── tests/                   # Tests unitaires
│   ├── test_sondages.py
│   └── test_reponses.py
├── app.py                   # Point d'entrée principal
├── config.py                # Configuration de l'application
├── requirements.txt         # Dépendances Python
└── README.md                # Documentation
```


## 🔧 Configuration

**Pour configurer la connexion à MongoDB, modifiez le fichier config.py :**

```python
    class Config:
    MONGO_URI = 'mongodb://localhost:27017/sondage_app'
```
## 🧪 Tests

**Les tests unitaires se trouvent dans le dossier tests/. Vous pouvez les exécuter avec pytest :**

```bash
    pytest
```
## ✨ Auteur

- Nom : **DontRobMe**
- GitHub : **https://github.com/DontRobMe**

## 📄 Licence

**Ce projet est sous licence MIT. Vous êtes libre de l'utiliser, de le modifier et de le distribuer.**


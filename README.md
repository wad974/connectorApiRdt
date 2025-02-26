Projet : Intégration API MyRDT vers Odoo

📌 Description

Ce projet vise à intégrer l'API MyRDT avec Odoo en utilisant FastAPI. L'objectif est de récupérer les commandes et documents depuis MyRDT et de les envoyer vers Odoo pour une gestion centralisée.

🚀 Technologies utilisées

FastAPI : Framework web en Python pour la gestion des APIs.

Requests : Pour interagir avec l'API MyRDT.

Pydantic : Pour la validation des données.

Odoo ORM : Pour l'intégration avec Odoo.

Dotenv : Pour gérer les variables d'environnement.

📂 Installation

1️⃣ Cloner le dépôt

git clone https://github.com/votre-repo.git
cd votre-repo

2️⃣ Créer un environnement virtuel

python -m venv venv
source venv/bin/activate  # Sur Linux/Macenv\Scripts\activate  # Sur Windows

3️⃣ Installer les dépendances

pip install -r requirements.txt

4️⃣ Configurer les variables d'environnement

Créer un fichier .env et y ajouter :

MY_RDT_URL=https://api.myrdt.com
MY_RDT_API_KEY=your_api_key_here

🔥 Lancer l'application

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

📌 Endpoints disponibles

Méthode

Endpoint

Description

GET

/commandes/

Récupérer les commandes MyRDT

POST

/documents/

Récupérer les documents MyRDT

📜 Schéma ASCII de l'architecture

              +-------------+
              |   Client    |
              +-------------+
                     |
                     v
       +----------------------+
       |  FastAPI Middleware  |
       | - Reçoit la requête  |
       | - Gère CORS et logs  |
       +----------------------+
                     |
                     v
       +----------------------+
       |   Authentification   |
       | - Vérifie l'API Key  |
       | - Rejette si invalide|
       +----------------------+
                     |
                     v
       +----------------------+
       |  API MyRDT (GET)     |
       | - Envoie requête API |
       | - Récupère données   |
       +----------------------+
                     |
                     v
       +----------------------+
       |  Traitement des      |
       |  commandes & docs    |
       | - Filtre les infos   |
       | - Formate les données|
       +----------------------+
                     |
                     v
       +----------------------+
       |    Intégration       |
       |      Odoo            |
       | - Enregistre données |
       | - Associe aux modèles|
       +----------------------+

✅ Sécurité

Authentification via clé API.

Contrôle des erreurs avec FastAPI.

Restriction des accès via CORS.

🛠 Améliorations possibles

Ajouter un cache pour éviter les appels répétés à MyRDT.

Améliorer la gestion des erreurs et logs.

Intégrer une synchronisation automatique avec Odoo.

📬 Support

Pour toute question ou amélioration, contactez-nous à : info.sdpma@sicalait.fr
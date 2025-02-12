#flask pour visualiser la connexion api
from flask import Flask, render_template, redirect, url_for


# -----------------------------------------------------------
# ✅ Initialisation de FLASK
# -----------------------------------------------------------
flask = Flask(__name__)

#route racine
@flask.route('/')
def home():
    return render_template('home.html')

#page filtres
@flask.route('/filtres')
def filtre():
    return "Les filtres"

#page tous les commandes
@flask.route('/touslescommandes')
def tous_les_commandes():
    return "Tous les commandes"

# -----------------------------------------------------------
# ✅ Lancer FastAPI et Flask en parallèle
# -----------------------------------------------------------
if __name__ == "__main__":
    flask.run(host="0.0.0.0", port=8888, debug=True)



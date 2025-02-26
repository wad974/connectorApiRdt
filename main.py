from fastapi import FastAPI, HTTPException, Security, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
import requests
import base64
import datetime
import os
from dotenv import load_dotenv
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import HTMLResponse


# Chargement des variables d'environnement
load_dotenv()

# Initialisation de l'API FastAPI
app = FastAPI()

# 📂 Dossier des templates HTML
templates = Jinja2Templates(directory="templates")

# 📂 Dossier des fichiers statiques (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

#home racine

#route racine
@app.get('/')
def home(request: Request):
    return templates.TemplateResponse(
        'base.html', 
        {
            'request' : request,
            'name' : 'sicalait'
        })

    
#page filtres
@app.get('/filtres')
async def filtre(request: Request):
    return templates.TemplateResponse(
        'base.html', 
        {
            'request' : request,
            'name' : 'sicalait'
        })

#page tous les commandes
@app.get('/touslescommandes')
async def tous_les_commandes(request: Request):
    return templates.TemplateResponse(
        'base.html', 
        {
            'request' : request,
            'name' : 'sicalait'
        })

# -----------------------------------------------------------
# ✅ Lancer FastAPI et Flask en parallèle
# -----------------------------------------------------------

@app.get('/')
async def home(request: Request):
    return templates.TemplateResponse('index.html', {'request' : request, 'name' : 'sicalait'})

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )


# Configuration CORS pour autoriser les requêtes depuis le front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser toutes les origines (mettre les URL spécifiques en prod)
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes HTTP
    allow_headers=["*"],  # Autoriser tous les en-têtes
)

# Récupération des variables d'environnement
MY_RDT_URL = os.getenv("MY_RDT_URL")
MY_RDT_API_KEY = os.getenv("MY_RDT_API_KEY")

# Vérification des variables requises
if not all([MY_RDT_URL, MY_RDT_API_KEY]):
    raise ValueError("Toutes les variables d'environnement (MY_RDT_URL et MY_RDT_API_KEY) doivent être définies.")

# Configuration de l'authentification par clé API
api_key_header = APIKeyHeader(name="key", auto_error=True)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    """
    Vérifie que la clé API est valide.
    """
    if api_key_header != MY_RDT_API_KEY:
        raise HTTPException(status_code=403, detail="Clé API invalide")
    return api_key_header

# Configuration des en-têtes pour les requêtes à l'API MyRdt
headers = {"key": MY_RDT_API_KEY}

# -----------------------------------------------------------
# ✅ ROUTE : Récupération des commandes
# -----------------------------------------------------------
@app.get("/commandes/")
def recupere_commandes():
    """
    Récupère la liste des commandes depuis l'API externe MyRDT.
    """
    try:
        response = requests.get(f"{MY_RDT_URL}/commandes", headers=headers)

        if response.status_code == 200:
            
            # a filtrer pour recuperer les fichier pour SLS :
            # numDossierClient - idArmateur - numDossierRdt - dateCommande
            # dateDepart - bl - idArmateur - numConteneur - navire
            
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Erreur API externe")

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erreur de connexion à MyRDT : {str(e)}")

# -----------------------------------------------------------
# ✅ MODÈLE Pydantic pour les documents de commande
# -----------------------------------------------------------
class Documents(BaseModel):
    site: str
    numDossierRdt: int
    siteImport: Optional[str] = None
    numDossierRdtImport: Optional[int] = None

# -----------------------------------------------------------
# ✅ ROUTE : Récupération des documents d'une commande
# FTP 172.17.71.161
# -----------------------------------------------------------
@app.post("/documents/")
async def recupere_documents(document: Documents):
    """
    Récupère les documents associés à une commande sous forme de fichier ZIP.
    """
    # Construction de l'URL pour récupérer les documents
    url_documents = (
        f"{MY_RDT_URL}/documents-commande?"
        f"site={document.site}&"
        f"numDossierRdt={document.numDossierRdt}&"
        f"siteImport={document.siteImport or ''}&"
        f"numDossierRdtImport={document.numDossierRdtImport or 0}"
    )

    try:
        # Requête GET vers l'API MyRDT
        response = requests.get(url_documents, headers=headers)

        if response.status_code == 200:
            data = response.json()

            if data["status"]:
                # Récupération du fichier ZIP encodé en base64
                base64_zip = data["data"]["fichier"]
                zip_data = base64.b64decode(base64_zip)

                # Création d'un nom de fichier unique
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"documents_commande_{timestamp}.zip"

                # Enregistrement du fichier ZIP
                with open(filename, "wb") as f:
                    f.write(zip_data)

                return {"message": f"Fichier enregistré sous : {filename}"}

            else:
                raise HTTPException(status_code=400, detail="Réponse API invalide ou fichier inexistant")

        else:
            raise HTTPException(status_code=response.status_code, detail="Erreur lors de la récupération des documents")

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erreur de connexion à MyRDT : {str(e)}")
    


# -----------------------------------------------------------
# ✅ Lancer FastAPI et Flask en parallèle
# -----------------------------------------------------------    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9999)
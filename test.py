from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader, APIKey
from fastapi.middleware.cors import CORSMiddleware
import xmlrpc.client
from typing import Optional
from pydantic import BaseModel
import datetime

#requests json
import requests
#base64
import base64


api = FastAPI()

import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Configuration CORS
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplacez par l'URL de votre front-end
    allow_credentials=True,
    allow_methods=["*"],  # Méthodes HTTP autorisées
    allow_headers=["*"],  # En-têtes autorisés
)

# Configuration MyRdt
url = os.getenv('MY_RDT_URL')
#selon le GET
commandes = 'commandes'
documents = 'documents-commande'
# Configuration API Key
API_KEY = os.getenv('MY_RDT_API_KEY')
#if not all([url, db, username, password, API_KEY]):

#on verifie que tous les paramétres sont Inscrit
if not all([url, API_KEY]):
    raise ValueError("Toutes les variables d'environnement (Odoo et API_KEY) doivent être définies")

#api key header authentification
api_key_header = APIKeyHeader(name="key", auto_error=True)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Clé API invalide"
        )
    return api_key_header


# Connexion MyRdt
# Header de la requête
headers = {
    "key": API_KEY  # clé api
}

#urlDoc = 'https://api.groupe-rdt.com:8443/myrdt/documents-commande?site=131&numDossierRdt=2413111809&siteImport=211&numDossierRdtImport=2521101499'


#class Commandes (BaseModel):
    #dateDepart : str #(DD/MM/YYYY)
    #dateFin : str #(DD/MM/YYYY)
    #bl : str
    #activite : str #M: Maritime, A: Aérien, R: Routier
    #status : int #1 : En attente de livraison à l'entrepôt, 2 : Livrée en entrepôt, 3 : Empotée, 4 : Flottante, 5 : Arrivée

#@app.post('/commandes/{bl}/')
@api.get('/commandes/')
#def recupereCommandes( bl: str, commande : Commandes ):
def recupereCommandes():
    
    #commande.bl = bl
    #recupere les données dans commandes
    #dateDepart = commande.dateDepart
    
    #Départ ou arrivé compris entre dateDebut et dateFin, ou flottant dans ce même intervalle. 
    #DateDebut et dateFin doivent être renseignés si un des deux l'est.
    #dateFin = commande.dateFin
    
    #Votre référence de commande, fournisseur, navire, vol, 
    #numéro de conteneur, port, BL
    #filtre = commande.bl
    #activite = commande.activite
    #status = commande.status
    
    # On fait une requête GET à l'API
    responseCommandes = requests.get(f'{url}/{commandes}', headers=headers)
    
    
    # Traitement de la réponse
    if responseCommandes.status_code == 200:
        
        return responseCommandes.json()
            
        if "data" in result:
            records = result["data"]
            #print(type(records))
            print(f"Nombre d'enregistrements : {len(records)}\n")
            
            #affichage mode csv
            # Parcourir et afficher chaque enregistrement
            for index , record in enumerate(records, start=1):
                
                #entête
                if index == 1 :
                    textEntrer = ""
                    
                    for key, value in record.items():
                        if textEntrer != "":
                            textEntrer = textEntrer + ";"
                            
                        textEntrer = textEntrer + key
                        
                    print(textEntrer)
                
                #data
                texteLigne = ""
                for key, value in record.items():
                    if texteLigne != "":
                        texteLigne = texteLigne + ";"
                        
                    texteLigne = texteLigne + '"' + f"{value}" + '"'
                    
                print(texteLigne)
                    
            print("")
            
            return textEntrer, texteLigne
    
        else:
            print("Erreur :", result.get("error", "Réponse inattendue"))
        
    
    else:
        raise HTTPException(status_code=responseCommandes.status_code, detail="Erreur API externe")
    
    ### FIN 
    '''
    #  On vérifie si la requête a réussi (status code 200)(Voir doc MyRDT pour les autres STATUS) 
    if responseCommandes.status_code == 200 :
        #print("Réponse de l'API:", response.json())
        #on stock la response json pour le travailler
        requeteCommande = responseCommandes.json()
        #print('réponse requete :', requete['data'])
        #order= []
        #boucle pour data
        for commande in requeteCommande['data']:
            
            #if filtre == commande['bl']:
                
                print('###############COMMANDE############')
                print('commande site : ', commande['site'])
                print('Numéros dossier : ', commande['numDossierRdt'])
                print('Nom Société : ', commande['desNom'])
                print('Type de Marchandise : ', commande['marchandises'])
                print('Date de la Commande : ', commande['dateCommande'])
                print('Date départ : ', commande['dateDepart'])
                print('Date départ : ', commande['dateArrivee'])
                print('Numéros Site Import: ', commande['siteImport'])
                print('Numéros Dossier Rdt Import: ', commande['numDossierRdtImport'])
                print('###################################')
                
                # Créer une nouvelle instance de Commandes avec les données de l'API
                
                order.append(Commandes(
                    #dateDebut = commande['dateDepart'],
                    #dateFin = commande['dateArrivee'],
                    bl = commande['bl'],
                    #activite = commande['activite'],
                    #status = commande['idTracing']
                    )
                )
                
                order.append({
                        'Site' : commande['site'],
                        'Nom Société' : commande['desNom'],
                        'Numéros dossier' : commande['numDossierRdt'],
                        'Numéros de commande' : commande['dateCommande'],
                        'Type de Marchandise' : commande['marchandises'],
                        'Numéros Site Import ' : commande['siteImport'], 
                        'Numéros Dossier Rdt Import ' :commande['numDossierRdtImport'],
                        'Tracing' : commande['tracing'],
                        'date de départ' : commande['dateDepart'],
                        'date d\'arriver' : commande['dateArrivee']
                })
                
                ### DEBUT 
                
                        
                
            #else: 
            #    print(f'Erreur : BL non présent dans cette commande')
        
    # Vérifier si la requête a réussi (status code 200)
    else:
        print(f"Erreur {responseCommandes.status_code} : {responseCommandes.text}")
    '''

##########################
#class documents commandes
class Documents(BaseModel): 
    site : str
    numDossierRdt : int
    siteImport : str = ''
    numDossierRdtImport : int = 0
#function appel getDocuments
@api.post('/documents/{site}{numDossierRdt}{siteImport}{numDossierRdtImport}')
def recupereDocuments( site:str, numDossierRdt:int, siteImport: str | None = None, numDossierRdtImport: int | None = None, document : Documents = None):
    #recupere les données dans documents

    site = document.site#str
    numDossierRdt = document.numDossierRdt#int
    siteImport = document.siteImport#str
    numDossierRdtImport = document.numDossierRdtImport#int
    
    #on construit l'url à injecter
    urlDoc = f'{url}/{documents}?\
        site={site}&\
        numDossierRdt={numDossierRdt}&\
        siteImport={siteImport}&\
        numDossierRdtImport={numDossierRdtImport}'
        
    #on appel la requete api Rdt
    requeteZip = requests.get(f'{urlDoc}', headers=headers)
    #reponseDocuments
    if requeteZip.status_code == 200:
        # On vas Récupérer le fichier ZIP encodé en base64 depuis la réponse JSON
        data = requeteZip.json()  # On vérifie que la réponse est en format JSON
        
        print('DATA BASE64 : ', data['data']['nom'])
        
        # Nom de base du fichier
        base_filename = "documents_commande"
        
        counterDocuments= ''
        dataCounterDocuments = datetime.datetime.now()
        dataCounterDocuments = dataCounterDocuments.strftime("%Y-%m-%d_%H:%M:%S") # format personnalisé
        filename = base_filename+'_'+dataCounterDocuments+'.zip'
        
        if data['status'] :
            
            print('OKAY DANS DATA')
            # Supposons que la clé contenant le ZIP soit 'base64_zip'
            base64_zip = data['data']['fichier']
            
            # Décoder le fichier ZIP depuis base64
            zip_data = base64.b64decode(base64_zip)
            
            # Vérifier si le fichier existe et incrémenter le nom
            while os.path.exists(filename):
                filename = f"documents_commande_{counterDocuments}.zip"
                counterDocuments += dataCounterDocuments
            
            # Enregistrer le fichier ZIP sur le disque avec un nom unique
            try:
                with open(filename, "wb") as f:  # Utilisation de "wb" au lieu de "xb"
                    f.write(zip_data)
                print(f"Le fichier ZIP a été téléchargé et enregistré sous : {filename}")
                
            except Exception as e:
                print(f"Erreur lors de l'écriture du fichier : {e}")
                
    else:
        print(f"Erreur {requeteZip.status_code} : {requeteZip.text}")

    return document






if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=9999)

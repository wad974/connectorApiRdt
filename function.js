// d'implémentation pour une requête GET
async function postData(url = "") {
    // Les options par défaut sont indiquées par *
    const response = await fetch(url, {
        method: "GET", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, *cors, same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, *same-origin, omit
        headers: {
            "Content-Type": "application/json",
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: "follow", // manual, *follow, error
        referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        //body: JSON.stringify(donnees), // le type utilisé pour le corps doit correspondre à l'en-tête "Content-Type"
    });
    return response.json(); // transforme la réponse JSON reçue en objet JavaScript natif
}


function afficheDiv(commande, index) {
    let contentdiv = document.createElement('div')

    contentdiv.setAttribute('class', 'contenu')
    //console.log(commande)
    contentdiv.innerHTML += `
                <h3>
                    <strong>N° DOSSIER / CDE ${index + 1} :</strong> ${commande.numDossierClient}
                    <p><strong>Marchandise</strong> : ${commande.marchandises}</p>
                </h3>
                <div class='bloc'> 
                    <div class="bloc-gauche"> 
                        <p>Compagnie Maritime : ${commande.idArmateur}</p> 
                        <p>Numéros Dossier Rdt : ${commande.numDossierRdt}</p>
                        <p> Sea Way Bill ( BL ) : ${commande.bl}</p>
                        <p>Référence Groupage: ${commande.refGroupage}</p>
                        <p>Groupage: ${commande.groupage}</p>
                    </div> 
                    <div class="bloc-droite">  
                        <p>Date Commande (ETD) : ${commande.dateCommande}</p>
                        <p>Date Départ (ETA) : ${commande.dateDepart}</p>
                        <p>Date Arrivée (BAE) : ${commande.dateArrivee}</p>
                        <p>Emballage : ${commande.emballage}</p>
                        <p>Nbre Colis : ${commande.nombreColis}</p>
                    </div>
                </div>
                <h5> Tracing : ${commande.tracing} <br>
                        Nom Navire : ${commande.navire}
                </h5>
                `;

    return contentdiv;
}

// funciton affiche data
function afficheData(donnees, txt) {
    

    donnees.data.forEach((commande, index) => {
        //console.log(commande.numDossierClient, txt)

        if (commande.groupage === txt) {
            
            let contentdiv = afficheDiv(commande, index);
            console.log('Groupage')
            filtreOutput.appendChild(contentdiv)
            
            
        } else if (commande.numDossierRdt === txt) {

            let contentdiv = afficheDiv(commande, index);
            console.log('numDossierRdt')
            filtreOutput.appendChild(contentdiv)
            
            
        } else if (commande.numDossierClient.includes(txt)) {
            //console.log(commande.numDossierClient, txt)
            
            let contentdiv = afficheDiv(commande, index);
            console.log('numDossierClient')
            filtreOutput.appendChild(contentdiv)
            

            
        } else if (commande.bl.includes(txt)) {
            console.log(commande.bl, txt)
            let contentdiv = afficheDiv(commande, index);
            console.log('bl')
            filtreOutput.appendChild(contentdiv)


            
        } else {

            let contentdiv = afficheDiv(commande, index);
            sortie.appendChild(contentdiv)

            console.log('AUCUN ARTICLE');
            console.log(filtreError)
            

        }

        
    });


    
}

// function patientez
function wait() {
    let loadingMessage = document.querySelectorAll('.await');
    loadingMessage.forEach(element => {
        element.innerHTML = "<p class='sablier'> <span class='anim'>⏳</span> Veuillez patienter, chargement en cours...</p>";
        element.style.display = "block";
    });
}

function pawait() {
    let loadingMessage = document.querySelectorAll('.await');
    loadingMessage.forEach(element => {
        element.innerHTML = "";
        element.style.display = "none";
    });
}




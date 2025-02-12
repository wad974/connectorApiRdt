// url api python
let url = 'http://0.0.0.0:9999/commandes/';
let sortie = document.querySelector('#output');
let mainOutput = document.querySelector('.mainOutput');
let await = document.querySelectorAll('.await')

// on recup allBouton
let input = document.querySelectorAll('.filtres input')
//console.log(input)

for (let index = 0; index < input.length; index++) {
    input[index].addEventListener('click', (event) => {
        event.target.value = ''
    })
}


/**BOUTON TOUS LES COMMANDES */

let bouton = document.querySelector('.button');

bouton.addEventListener('click', async (event) => {
    event.preventDefault();

    if (filtres.style.display = 'block') {
        filtres.style.display = 'none'
        mainOutput.style.display = 'block'
    }

    // message de chargement
    wait()

    // ici fuuntion post data
    postData(url).then((donnees) => {
        console.log(donnees); // Les données JSON analysées par l'appel `donnees.json()`

        let sortieStatus = document.querySelector('#status');
        let sortieMessage = document.querySelector('#message');

        // Affichage du status
        sortieStatus.innerHTML = 'MyRdt Status : ' + donnees.status;
        // Affichage du message
        sortieMessage.innerHTML = 'MyRdt Message : ' + donnees.message;

        // Vérifier si "data" existe et n'est pas vide
        if (donnees.data && donnees.data.length > 0) {
            sortie.innerHTML = ""; // Vider avant d'ajouter
            // on affiche la function AfficheData
            afficheData(donnees);

        } else {
            sortie.innerHTML = "<p>Aucune commande trouvée.</p>";
        }

        // on retire message de chargement
        pawait();
    });

});



/*BOUTON  FILTRES*/
let boutonFiltre = document.querySelector('.buttonFiltres')
let filtres = document.querySelector('.filtres')
let filtreOutput = document.querySelector('#filtreOutput')
let filtreError = document.querySelector('#filtreError')

filtres.style.display = 'none'

boutonFiltre.addEventListener('click', (event) => {
    event.preventDefault();

    sortie.innerHTML = ''
    filtreOutput.innerHTML = ''

    if (filtres.style.display = 'none') {
        filtres.style.display = 'block'
        mainOutput.style.display = 'none'
    }

    let inputNumDossier = document.querySelector('.numDossier')
    //let inputNumDossierClient = document.querySelector('.numDossierClient')
    //let inputGroupage = document.querySelector('.groupage')
    //let inputBl = document.querySelector('.bl')


    inputNumDossier.addEventListener('keydown', (event) => {

        if (event.key === "Enter") {

            event.preventDefault();
            event.stopPropagation();

            let texte = event.target.value;
            texte = parseInt(texte)
            console.log('texte', texte)

            //affiche message chargement
            wait();

            sortie.innerHTML = ''
            filtreOutput.innerHTML = ''

            // ici fuuntion post data FILTRES
            postData(url).then((donnees) => {
                console.log(donnees); // Les données JSON analysées par l'appel `donnees.json()`

                let sortieStatus = document.querySelector('#status');
                let sortieMessage = document.querySelector('#message');

                // Affichage du status
                //sortieStatus.innerHTML = 'MyRdt Status : ' + donnees.status;
                // Affichage du message
                //sortieMessage.innerHTML = 'MyRdt Message : ' + donnees.message;

                // Vérifier si "data" existe et n'est pas vide
                if (donnees.data && donnees.data.length > 0) {
                    sortie.innerHTML = ""; // Vider avant d'ajouter
                    // on affiche la function AfficheData
                    //console.log('texte', texte)
                    afficheData(donnees, texte);

                } else {
                    sortie.innerHTML = "<p>Aucune commande trouvée.</p>";
                }

                // on retire message chargement
                pawait();
            });

        }
    });

});
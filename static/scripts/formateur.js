function afficherModalAjouterDate(formattedDate) {
    const modal = document.createElement('div');
    modal.classList.add('modal');
    modal.innerHTML = `
        <div class="modal-content">
    <span class="close" onclick="fermerModal()">&times;</span>
    <h2>Ajouter une date</h2>
    <label for="newDate">Date :</label>
    <input type="datetime-local" id="newDate" name="newDate" value="${formattedDate}"><br><br>
    <label for="duree">Durée :</label>
    <input type="time" id="duree" name="duree" value="00:00" min="00:00" max="05:00" step="1800"><br><br>
    <input type="checkbox" id="pauseCheckbox" onchange="afficherChampsPause()"> Pause<br><br>
    <div id="champsPause" style="display: none;">
        <label for="pauseDebut">Début de la pause :</label>
        <input type="time" id="pauseDebut" name="pauseDebut" value="${formattedDate}"><br><br>
        <label for="pauseDuree">Durée de la pause :</label>
        <input type="time" id="pauseDuree" name="pauseDuree" value="00:00" min="00:00" max="05:00" step="1800"><br><br>
    </div>
    <button id="ajouterButton">Ajouter</button>
</div>

        
    `;
    document.body.appendChild(modal);

    // Ajouter un écouteur d'événements au bouton dans le contexte de la fenêtre modale
    modal.querySelector('#ajouterButton').addEventListener('click', ajouterDate);
}

function afficherModalDetailsRdv(details) {
    const modal = document.createElement('div');
    modal.classList.add('modal');
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close" onclick="fermerModal()">&times;</span>
            <h2>${details.titre}</h2>
            <p>Durée : ${details.duree} heure(s)</p>
            <p>${details.nom} ${details.prenom}</p>
            <p>Tel : ${details.telephone}</p>
            <p>Mail : ${details.email}</p>
            <button id="supprimerButton">Supprimer</button>
        </div>
    `;
    document.body.appendChild(modal);

    // Ajouter un écouteur d'événements au bouton de suppression dans le contexte de la fenêtre modale
    modal.querySelector('#supprimerButton').addEventListener('click', function () {
        supprimerRdv(details.rdv);
    });
}

function fermerModal() {
    const modal = document.querySelector('.modal');
    modal.parentNode.removeChild(modal);
}

function ajouterDate() {
    // Récupérer la valeur de l'input de date
    var newDateValue = document.getElementById('newDate').value;
    var dureeValue = document.getElementById('duree').value;
    var pauseDebut = document.getElementById('pauseDebut').value;
    var pauseDuree = document.getElementById('pauseDuree').value;
    var pauseCheckbox = document.getElementById('pauseCheckbox').checked;


    // Créer un objet contenant les données à envoyer
    var data = {
        debut: newDateValue,
        duree: dureeValue,
        debutpause: pauseDebut,
        dureepause: pauseDuree,
        pause: pauseCheckbox,
    };

    // Créer une requête HTTP POST
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/ajouterrdv', true);

    // Définir l'en-tête de la requête
    xhr.setRequestHeader('Content-Type', 'application/json');

    // Réagir lorsque la requête est terminée
    xhr.onload = function () {
        if (xhr.status === 200) {
            // La requête a réussi
            console.log('Date ajoutée avec succès !');
            window.location.reload();
        } else {
            // La requête a échoué
            console.error('Échec de l\'ajout de la date.');
        }
        // Fermer la fenêtre modale
        fermerModal();
    };

    // Envoyer la requête avec les données JSON
    xhr.send(JSON.stringify(data));
}

function supprimerRdv(id_rdv) {
    // Envoyer une requête au backend pour supprimer le rendez-vous avec l'identifiant idRdv
    fetch('/supprimer_rdv', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id_rdv: id_rdv })
    })
    .then(response => {
        if (response.ok) {
            // Si la suppression est réussie, actualiser la page ou rediriger l'utilisateur
            window.location.reload(); // Vous pouvez remplacer cela par une redirection appropriée
        } else {
            console.error('La suppression du rendez-vous a échoué.');
        }
    })
    .catch(error => {
        console.error('Erreur lors de la suppression du rendez-vous :', error);
    });

    // Fermer la fenêtre modale
    fermerModal();
}

function afficherChampsPause() {
            var checkBox = document.getElementById("pauseCheckbox");
            var champsPause = document.getElementById("champsPause");
            if (checkBox.checked == true) {
                champsPause.style.display = "block";
            } else {
                champsPause.style.display = "none";
            }
        }
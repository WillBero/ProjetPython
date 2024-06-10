
var currentPage = 'accueil';

// GESTION DES PAGES

document.addEventListener('DOMContentLoaded', function () {
    // Masquer toutes les pages sauf la première
    masquerToutesLesPages();
    document.getElementById('accueil').style.display = 'block';
});


function afficherPage(pageId) {
    
    // Masquer toutes les pages
    masquerToutesLesPages();
    // Afficher la page spécifiée
    document.getElementById(pageId).style.display = 'block';

    // Mettre à jour la variable currentPage
}

function masquerToutesLesPages() {
    // Masquer toutes les pages
    var pages = document.getElementsByClassName('page');
    for (var i = 0; i < pages.length; i++) {
        pages[i].style.display = 'none';
    }
}


function afficherInfosCentre(id_centre) {
    if (id_centre) {
        // Récupérer les formateurs associés au centre sélectionné depuis la base de données
        fetch(`/centres/${id_centre}`)
            .then(response => response.json())
            .then(data => {
                // Effacer le contenu précédent
                const formateursList = document.getElementById('formateursList');
                formateursList.innerHTML = '';

                // Générer des éléments li pour chaque formateur et les ajouter à la liste
                data.forEach((formateur) => {
                    const li = document.createElement('li');
                    li.textContent = formateur.nom + ' ' + formateur.prenom;
                    li.onclick = function () {
                        afficherInfosFormateur(formateur.id_formateur); // Appeler la fonction pour afficher les infos du formateur avec son ID
                    };
                    formateursList.appendChild(li);
                });
            })
            .catch(error => {
                console.error('Erreur lors de la récupération des formateurs :', error);
            });

        // Afficher la barre des formateurs du centre
        document.getElementById('formateursBar').style.display = 'block';
    } else {
        // Masquer la barre des formateurs si aucun centre n'est sélectionné
        document.getElementById('formateursBar').style.display = 'none';
    }
}


function afficherInfosFormateur(id_formateur) {
    if (id_formateur) {
        fetch(`/formateurs/${id_formateur}/rdv`)
            .then(response => response.json())
            .then(data => {
                const events = data.map(rdv => ({
                    title: "Rendez-vous disponible",
                    start: rdv.debut, // Format : 'YYYY-MM-DD'
                    id: rdv.id_rdv,
                    end: rdv.fin,
                }));

                const calendarEl = document.getElementById('calendar2');
                const calendar = new FullCalendar.Calendar(calendarEl, {
                    weekends: false,
                    allDaySlot: false,
                    initialView: 'timeGridWeek',
                    slotMinTime: '07:00:00',
                    slotMaxTime: '18:00:00',
                    locale: 'fr',
                    headerToolbar: {
                        left: 'prev,next today',
                        center: 'title',
                        right: 'dayGridMonth,timeGridWeek,timeGridDay,listYear'
                    },
                    buttonText: {
                        today: 'Aujourd\'hui',
                        month: 'Mois',
                        week: 'Semaines',
                        day: 'Jours',
                        list: 'Liste'
                    },
                    events: events,
                    eventClick: function (info) {
                        console.log("Event clicked:", info.event);
                        // Ouvrir une fenêtre modale au lieu d'une fenêtre pop-up
                        afficherModal(info.event);
                    }
                });

                calendar.render();
                calendarEl.style.display = 'block';
            })
            .catch(error => {
                console.error('Erreur lors de la récupération des rendez-vous du formateur :', error);
            });

        document.getElementById('infosFormateur').style.display = 'block';
    } else {
        document.getElementById('infosFormateur').style.display = 'none';
    }
}

function afficherModal(event) {
    const modal = document.createElement('div');
    modal.classList.add('modal');

    // Extraire les heures et les minutes de l'heure de début et de fin de l'événement
    const startHour = ('0' + event.start.getHours()).slice(-2);
    const startMinute = ('0' + event.start.getMinutes()).slice(-2);
    const endHour = ('0' + event.end.getHours()).slice(-2);
    const endMinute = ('0' + event.end.getMinutes()).slice(-2);

    modal.innerHTML = `
        <div class="modal-content">
            <span class="close" onclick="fermerModal()">&times;</span>
            <h2>${event.title}</h2>
            <form id="rendezVousForm">
                <div class="form-group">
                    <label for="heureDebut">Heure de début :</label>
                    <input type="time" id="heureDebut" name="heureDebut" required min="${startHour}:${startMinute}" max="${endHour}:${endMinute}">
                </div>
                <div class="form-group">
                    <label for="heureFin">Heure de fin :</label>
                    <input type="time" id="heureFin" name="heureFin" required min="${startHour}:${startMinute}" max="${endHour}:${endMinute}">
                </div>
                <div class="form-group">
                    <label for="nomRdv">Nom :</label>
                    <input type="text" id="nomRdv" name="nomRdv" placeholder="Entrez votre nom" required>
                </div>
                <div class="form-group">
                    <label for="prenomRdv">Prénom :</label>
                    <input type="text" id="prenomRdv" name="prenomRdv" placeholder="Entrez votre prénom" required>
                </div>
                <div class="form-group">
                    <label for="emailRdv">Email :</label>
                    <input type="email" id="emailRdv" name="emailRdv" placeholder="Entrez votre email" required>
                </div>
                <div class="form-group">
                    <label for="telephoneRdv">Téléphone :</label>
                    <input type="tel" id="telephoneRdv" name="telephoneRdv" placeholder="Entrez votre téléphone" required>
                </div>
                <div class="form-group">
                    <label for="formationRdv">Sélectionnez une formation :</label>
                    <select id="formationRdv" name="formationRdv" required>
                        <option value="1">LP RGI</option>
                        <option value="2">Externe</option>
                    </select>
                </div>
                <button id="button">Prendre rendez-vous</button>
            </form>
        </div>
    `;
    document.body.appendChild(modal);

    // Ajouter un écouteur d'événements au bouton de validation dans le modal
    modal.querySelector('#button').addEventListener('click', function () {
        prendreRdv(event.id);
    });
}

function fermerModal() {
    const modal = document.querySelector('.modal');
    modal.parentNode.removeChild(modal);
}

function formatDate(date) {
    const options = { day: 'numeric', month: 'long', year: 'numeric', hour: 'numeric', minute: 'numeric' };
    return new Date(date).toLocaleDateString('fr-FR', options);
}

function prendreRdv(id_rdv) {
    var nom = document.getElementById('nomRdv').value;
    var prenom = document.getElementById('prenomRdv').value;
    var email = document.getElementById('emailRdv').value;
    var telephone = document.getElementById('telephoneRdv').value;
    var id_formation = document.getElementById('formationRdv').value;
    var heureDebut = document.getElementById('heureDebut').value;
    var heureFin = document.getElementById('heureFin').value;

    // Envoyer les données du formulaire à la route /prendrerdv
    fetch(`/prendrerdv`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nom: nom,
            prenom: prenom,
            email: email,
            telephone: telephone,
            id_formation: id_formation,
            id_rdv: id_rdv,
            heureDebut: heureDebut,
            heureFin: heureFin
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); // Afficher le message renvoyé par le serveur
        // Vous pouvez également afficher un message à l'utilisateur pour confirmer que le rendez-vous a été pris
        alert('Rendez-vous enregistré avec succès !');
        // Vous pouvez également rediriger l'utilisateur vers une autre page si nécessaire
        // window.location.href = '/autre_page';
    })
    .catch(error => {
        console.error('Erreur lors de l\'inscription au rendez-vous :', error);
        // Afficher un message d'erreur à l'utilisateur si nécessaire
        alert('Erreur lors de l\'inscription au rendez-vous. Veuillez réessayer.');
    });
}
// GESTION DES RDV du formateur








// AUTRE

function envoyerEmail() {
    var nom = document.getElementById('nom').value;
    var email = document.getElementById('email').value;
    var message = document.getElementById('message').value;
    var id_formateur = document.getElementById('formateur').value;
    var prenom = document.getElementById('prenom').value;

    fetch('/contact', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nom: nom, email: email, id_formateur: id_formateur, prenom: prenom, message: message, })
    })
        .then(response => {
            if (response.ok) {
                document.getElementById('messageSucces').style.display = 'block'; 
                document.getElementById('contactForm').reset(); // Vider le formulaire
                // Afficher le message de succès
                return response.json();
            }
            throw new Error('Erreur lors de l\'envoi des données');
        })
        .then(data => {
            console.log('Données envoyées avec succès :', data);
        })
        .catch(error => {
            console.error('Erreur lors de l\'envoi des données :', error);
        });
}





document.getElementById('connexionForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Empêche l'envoi du formulaire de manière traditionnelle
    
    var form = event.target;
    var formData = new FormData(form);
    var errorMessageDiv = document.getElementById('error-message');
    errorMessageDiv.textContent = ''; // Efface les messages d'erreur précédents

    fetch('/connexion', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Rediriger vers la page du formateur
            window.location.href = data.redirect;
        } else {
            // Afficher le message d'erreur
            errorMessageDiv.textContent = data.error;
        }
    })
    .catch(error => {
        console.error('Erreur lors de la soumission du formulaire:', error);
        errorMessageDiv.textContent = 'Une erreur est survenue. Veuillez réessayer plus tard.';
    });
});




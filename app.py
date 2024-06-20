from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail, Message
import pymysql.cursors
import time
import os
from dotenv import load_dotenv
import bcrypt
from pony.orm import Database, PrimaryKey, Required, Optional, Set, db_session, select, commit

load_dotenv()

app = Flask(__name__)
app.config.update(
MAIL_SERVER = os.getenv("MAIL_SERVER"),
MAIL_PORT = os.getenv("MAIL_PORT"),
MAIL_USE_SSL = os.getenv("MAIL_USE_SSL"),
MAIL_USERNAME = os.getenv("MAIL_USERNAME") ,
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
)

mail = Mail(app)   

app.secret_key =  os.getenv("APP_SECRET_KEY")


db = Database()

class Centres(db.Entity):
    id_centre = PrimaryKey(int, auto=True)
    ville = Optional(str, 20)
    formateurs = Set('Formateurs_centres')

class Contacts(db.Entity):
    id_contact = PrimaryKey(int, auto=True)
    nom = Required(str, 20)
    email = Required(str, 25)
    date = Required(datetime)
    id_formateur = Optional('Formateurs')
    prenom = Optional(str, 20)
    message = Optional(str)

class Formateurs(db.Entity):
    id_formateur = PrimaryKey(int, auto=True)
    nom = Optional(str, 20)
    prenom = Optional(str, 20)
    email = Optional(str, 25)
    mdp = Optional(str, 255)
    telephone = Optional(str, 10)
    contacts = Set(Contacts)
    centres = Set('Formateurs_centres')
    rdv = Set('Rdv')

class Formateurs_centres(db.Entity):
    id_formateur = Required(Formateurs)
    id_centre = Required(Centres)
    PrimaryKey(id_formateur, id_centre)

class Formations(db.Entity):
    id_formation = PrimaryKey(int, auto=True)
    nom = Optional(str, 15)
    rdv = Set('Rdv')

class Rdv(db.Entity):
    id_rdv = PrimaryKey(int, auto=True)
    debut = Optional(datetime)
    fin = Optional(datetime)
    nom = Optional(str, 20, nullable=True)
    prenom = Optional(str, 20, nullable=True)
    email = Optional(str, 25, nullable=True)
    telephone = Optional(str, 10 , nullable=True)
    id_formation = Optional(Formations)
    id_formateur = Required(Formateurs)

db.bind(provider='mysql', host=os.getenv("host"), user=os.getenv("user"), passwd=os.getenv("password"), db=os.getenv("db"),)
db.generate_mapping(create_tables=False)

@app.route('/')
@db_session
def index():
    # Utiliser Pony ORM pour obtenir les données nécessaires
    with db_session:
        formations = select(f for f in Formations)[:]
        centres = select(c for c in Centres)[:]
        formateurs = select(f for f in Formateurs)[:]

    # Convertir les objets de Pony ORM en dictionnaires pour les passer au template
    formations_dict = [f.to_dict() for f in formations]
    centres_dict = [c.to_dict() for c in centres]
    formateurs_dict = [f.to_dict() for f in formateurs]

    return render_template('index.jinja', centres=centres_dict, formations=formations_dict, formateur=formateurs_dict)


@app.route('/contact', methods=['POST'])
@db_session
def contact():
    data = request.get_json()
    nom = data['nom']
    email_e = data['email']
    prenom = data['prenom']
    message = data['message']
    id_formateur = int(data['id_formateur'])

    # Récupère l'email du formateur à partir de l'ID du formateur
    with db_session:
        formateur = Formateurs.get(id_formateur=id_formateur)
        if formateur:
            formateur_email = formateur.email
        else:
            return jsonify({'error': 'Formateur non trouvé'})

        # Enregistre le contact dans la base de données en utilisant Pony ORM
        contact = Contacts(
            nom=nom,
            prenom=prenom,
            email=email_e,
            message=message,
            date=datetime.now(),
            id_formateur=formateur
        )
        commit()  # Commit pour sauvegarder les changements dans la base de données

    # Envoie l'email au formateur
    msg = Message(
        body=f"{message}\n email : {email_e} \n nom: {nom} \n prenom {prenom}",
        recipients=[formateur_email],
        sender='flaskdoodle60@gmail.com',
        subject=f"Message de {prenom} {nom}"
    )
    mail.send(msg)

    return jsonify({'message': 'Message envoyé avec succès !'})



@app.route('/centres/<int:centre_id>')
@db_session
def formateurs(centre_id):
    # Sélectionne les formateurs liés au centre spécifique en utilisant Pony ORM
    formateurs_dict = select(f for fc in Formateurs_centres for f in fc.id_formateur if fc.id_centre.id_centre == centre_id).order_by(Formateurs.id_formateur)[:]

    # Convertit les objets en dictionnaires pour la réponse JSON
    formateurs_list = [
        {
            'id_formateur': f.id_formateur,
            'nom': f.nom,
            'prenom': f.prenom,
            'email': f.email,
            'telephone': f.telephone,
            # Ajoute d'autres champs si nécessaire
        }
        for f in formateurs_dict
    ]

    return jsonify(formateurs_list)

@app.route('/formateurs/<int:formateur_id>/rdv')
@db_session
def rendez_vous(formateur_id):
    maintenant = datetime.now()

    # Utilisation de Pony ORM pour sélectionner les rendez-vous
    rdvs = select(r for r in Rdv if r.id_formateur.id_formateur == formateur_id and r.debut >= maintenant and r.nom is None).order_by(Rdv.debut)[:]

    # Convertir les objets Rdv en dictionnaires pour la réponse JSON
    rdvs_list = [
        {
            'id_rdv': rdv.id_rdv,
            'debut': rdv.debut.strftime('%Y-%m-%d %H:%M:%S'),
            'fin': rdv.fin.strftime('%Y-%m-%d %H:%M:%S'),
            'nom': rdv.nom,
            'prenom': rdv.prenom,
            # Ajouter d'autres champs si nécessaire
        }
        for rdv in rdvs
    ]

    return jsonify(rdvs_list)


@app.route('/prendrerdv', methods=['POST'])
@db_session
def prendre_rdv():
    # Récupérer les données du formulaire
    nom = request.json.get('nom')
    prenom = request.json.get('prenom')
    email = request.json.get('email')
    telephone = request.json.get('telephone')
    id_formation = request.json.get('id_formation')
    id_rdv = request.json.get('id_rdv')
    heure_debut_str = request.json.get('heureDebut')  # Nouvelle heure de début
    heure_fin_str = request.json.get('heureFin')      # Nouvelle heure de fin
    heure_debut = datetime.strptime(heure_debut_str, '%H:%M').time()
    heure_fin = datetime.strptime(heure_fin_str, '%H:%M').time()

    # Récupérer les informations sur le rendez-vous existant
    rdv = Rdv.get(id_rdv=id_rdv)
    if rdv:
        id_formateur = rdv.id_formateur.id_formateur
        ancien_debut = rdv.debut
        ancienne_fin = rdv.fin

        nouvelle_heure_debut = datetime.combine(ancien_debut.date(), heure_debut)
        nouvelle_heure_fin = datetime.combine(ancienne_fin.date(), heure_fin)

        if ancien_debut == nouvelle_heure_debut and ancienne_fin == nouvelle_heure_fin:
            # Mettre à jour le rendez-vous existant avec les nouvelles heures de début et de fin
            rdv.nom = nom
            rdv.prenom = prenom
            rdv.email = email
            rdv.telephone = telephone
            rdv.debut = nouvelle_heure_debut
            rdv.fin = nouvelle_heure_fin
            commit()
        elif ancien_debut == nouvelle_heure_debut and nouvelle_heure_fin < ancienne_fin:
            # Créer le rendez-vous avant (s'il y a lieu)
            rdv.nom = nom
            rdv.prenom = prenom
            rdv.email = email
            rdv.telephone = telephone
            rdv.debut = nouvelle_heure_debut
            rdv.fin = nouvelle_heure_fin
            commit()

            # Créer un nouveau rendez-vous après la pause
            Rdv(id_formateur=rdv.id_formateur, debut=nouvelle_heure_fin, fin=ancienne_fin , nom = None, prenom = None, email = None, telephone = None)
            commit()
        elif nouvelle_heure_debut > ancien_debut and nouvelle_heure_fin < ancienne_fin:
            # Créer le rendez-vous après (s'il y a lieu)
            rdv.nom = nom
            rdv.prenom = prenom
            rdv.email = email
            rdv.telephone = telephone
            rdv.debut = nouvelle_heure_debut
            rdv.fin = nouvelle_heure_fin
            commit()

            # Créer un nouveau rendez-vous avant la pause
            Rdv(id_formateur=rdv.id_formateur, debut=ancien_debut, fin=nouvelle_heure_debut, nom = None, prenom = None, email = None, telephone = None)
            commit()
        else:
            # Mettre à jour le rendez-vous existant avec les nouvelles heures de début et de fin
            rdv.nom = nom
            rdv.prenom = prenom
            rdv.email = email
            rdv.telephone = telephone
            rdv.debut = nouvelle_heure_debut
            rdv.fin = nouvelle_heure_fin
            commit()

            # Créer un nouveau rendez-vous avant la pause
            Rdv(id_formateur=rdv.id_formateur, debut=ancien_debut, fin=nouvelle_heure_debut, nom = None, prenom = None, email = None, telephone = None)
            commit()

            # Créer un nouveau rendez-vous après la pause
            Rdv(id_formateur=rdv.id_formateur, debut=nouvelle_heure_fin, fin=ancienne_fin, nom = None, prenom = None, email = None, telephone = None)
            commit()

    # Récupérer l'e-mail du formateur à partir de son ID
    formateur = Formateurs.get(id_formateur=id_formateur)
    formateur_email = formateur.email

    # Récupérer le nom de la formation à partir de son ID
    formation = Formations.get(id_formation=id_formation)
    formation_nom = formation.nom

    # Envoyer un e-mail au formateur
    msg = Message(body=f"Monsieur/Madame {nom} a pris rendez-vous avec vous à la date du {nouvelle_heure_debut}. Son numéro de téléphone est : {telephone}\nSon adresse e-mail est : {email}\n{formation_nom}",
                  recipients=[formateur_email],
                  sender='flaskdoodle60@gmail.com',
                  subject="rendez-vouspris")

    mail.send(msg)

    # Rediriger l'utilisateur vers une page appropriée (par exemple, la page d'accueil)
    return jsonify({'message': 'Rendez-vous enregistré avec succès!'})

@app.route('/connexion', methods=['POST'])
@db_session
def connexion():
    email = request.form.get('emailConnexion')
    password = request.form.get('password')

    # Recherche du formateur dans la base de données avec Pony ORM
    formateur = select(f for f in Formateurs if f.email == email).first()

    if formateur and bcrypt.checkpw(password.encode('utf-8'), formateur.mdp.encode('utf-8')):
        # Identifiants valides, démarrer une session pour le formateur
        session['formateur_id'] = formateur.id_formateur
        return jsonify({'success': True, 'redirect': url_for('formateur')})
    else:
        # Identifiants invalides, retourner une réponse JSON avec un message d'erreur
        return jsonify({'success': False, 'error': 'Identifiant ou mot de passe invalide.'})
    
@app.route('/formateur')
@db_session
def formateur():
    formateur_id = session.get('formateur_id')

    # Sélectionner les rendez-vous pris par le formateur
    rdv_pris = select(r for r in Rdv if r.id_formateur.id_formateur == formateur_id and r.nom is not None and r.prenom is not None)[:]

    # Sélectionner les rendez-vous non pris par le formateur
    rdv_nonpris = select(r for r in Rdv if r.id_formateur.id_formateur == formateur_id and (r.nom is None or r.prenom is None))[:]

    # Sélectionner les informations du formateur
    formateur = Formateurs.get(id_formateur=formateur_id)

    return render_template('formateur.jinja', formateur=formateur, rdv_pris=rdv_pris, rdv_nonpris=rdv_nonpris)


@app.route('/supprimer_rdv', methods=['POST'])
@db_session
def supprimer_rdv():
    id_rdv = request.json.get('id_rdv')

    rdv = Rdv.get(id_rdv=id_rdv)
    # Supprimer le rendez-vous correspondant à l'id_rdv
    rdv.delete()

    # Commit pour sauvegarder les changements
    commit()

    return redirect('/')


@app.route('/deconnexion', methods=['POST'])
def deconnexion():
    # Supprimer la session de l'utilisateur
    session.pop('formateur_id', None)
    
    # Rediriger l'utilisateur vers la page d'accueil
    return redirect('/')

@app.route('/ajouterrdv', methods=['POST'])
@db_session
def ajouterrdv():
    # Récupérer les données envoyées par la requête POST
    date_str = request.json.get('debut')
    duree_str = request.json.get('duree')
    formateur_id = session.get('formateur_id')
    debutpause_str = request.json.get('debutpause')
    dureepause_str = request.json.get('dureepause')
    pause = request.json.get('pause')

    # Convertir la date reçue en objet datetime
    date_debut = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')

    # Convertir la durée en un objet timedelta
    duree_hour, duree_minute = map(int, duree_str.split(':'))
    duree_timedelta = timedelta(hours=duree_hour, minutes=duree_minute)

    # Calculer la date de fin en ajoutant la durée à la date de début
    date_fin = date_debut + duree_timedelta

    if date_debut >= datetime.now():
        if pause == False:  # Vérifie si aucune pause n'est spécifiée
            Rdv(debut=date_debut, fin=date_fin, id_formateur=formateur_id)
        else:
            debutpauses = datetime.strptime(debutpause_str, "%H:%M")
            debutpause = date_debut.replace(hour=debutpauses.hour, minute=debutpauses.minute)
            dureepause_hour, dureepause_minute = map(int, dureepause_str.split(':'))
            dureepause_timedelta = timedelta(hours=dureepause_hour, minutes=dureepause_minute)
            finpause = debutpause + dureepause_timedelta

            if date_debut < debutpause or finpause > date_fin:
                Rdv(debut=date_debut, fin=debutpause, id_formateur=formateur_id)
                Rdv(debut=finpause, fin=date_fin, id_formateur=formateur_id, nom=None, prenom=None, email=None, telephone=None)
            else:
                return jsonify({'error': 'la pause ne peut pas être pris avant la date debut'})
    else:
        return jsonify({'error': 'la date de début ne peut être antérieur à la date actuelle'})

    # Rediriger l'utilisateur vers la page d'accueil après l'ajout du rendez-vous
    return redirect('/')





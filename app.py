from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail, Message
import pymysql.cursors
import time
import os
from dotenv import load_dotenv
import bcrypt

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


connection = pymysql.connect(host=os.getenv("host"),
                            user=os.getenv("user"),
                            password=os.getenv("password"),
                            db=os.getenv("db"),
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def index():


    with connection.cursor() as cursor:
            sql = "SELECT * FROM formations"
            cursor.execute(sql)
            formations = cursor.fetchall()

    with connection.cursor() as cursor:
            sql1="SELECT * from centres"
            cursor.execute(sql1)
            centres= cursor.fetchall()

    with connection.cursor() as cursor:
            sql2="SELECT * from formateurs"
            cursor.execute(sql2)
            formateur= cursor.fetchall()

    
    return render_template('index.jinja', centres=centres, formations=formations, formateur=formateur)

@app.route('/contact', methods=['POST'])
def contact():

    data = request.get_json()
    nom = data['nom']
    email_e = data['email']
    prenom = data['prenom']
    message = data['message']
    id_formateur = int(data['id_formateur'])

    with connection.cursor() as cursor:
        sql = "SELECT email FROM formateurs WHERE id_formateur = %s"
        cursor.execute(sql, (id_formateur,))
        formateur_email = cursor.fetchone()['email']

    with connection.cursor() as cursor:
        sql1 = "INSERT INTO contacts (nom, prenom, email,message,date,id_formateur) VALUES (%s, %s,%s,%s,%s,%s)"
        cursor.execute(sql1, (nom,prenom,email_e,message, datetime.now(),id_formateur))
        connection.commit()

    msg = Message(body=f"{message}\n email : {email_e} \n nom: {nom} \n prenom {prenom}",
                 recipients=[formateur_email],
                 sender= 'flaskdoodle60@gmail.com',
                 subject=f"Message de {prenom} {nom}")
   
    mail.send(msg)
    
    return jsonify({'message': 'Rendez-vous enregistré avec succès !'})



@app.route('/centres/<int:centre_id>')
def formateurs(centre_id):

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM formateurs JOIN formateurs_centres ON formateurs.id_formateur = formateurs_centres.id_formateur WHERE formateurs_centres.id_centre = %s"
            cursor.execute(sql, (centre_id,))
            formateurs_list = cursor.fetchall()
    finally:
        connection.commit()

    return jsonify(formateurs_list)

@app.route('/formateurs/<int:formateur_id>/rdv')
def rendez_vous(formateur_id):
    maintenant = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id_rdv, debut, nom, prenom, fin FROM rdv WHERE id_formateur = %s AND debut >= %s AND nom IS NULL ORDER BY debut"
            cursor.execute(sql, (formateur_id, maintenant))
            rdvs_list = cursor.fetchall()

            # Convertir les dates en chaînes de caractères
            for rdv in rdvs_list:
                rdv['debut'] = rdv['debut'].strftime('%Y-%m-%d %H:%M:%S')
                rdv['fin'] = rdv['fin'].strftime('%Y-%m-%d %H:%M:%S')
                
    finally:
        connection.commit()

    return jsonify(rdvs_list)


@app.route('/prendrerdv', methods=['POST'])
def prendre_rdv():
    # Récupérer les données du formulaire
    nom = request.json.get('nom')
    prenom = request.json.get('prenom')
    email = request.json.get('email')
    telephone = request.json.get('telephone')
    id_formation = request.json.get('id_formation')
    id_rdv = request.json.get('id_rdv')
    heure_debut_str  = request.json.get('heureDebut')  # Nouvelle heure de début
    heure_fin_str = request.json.get('heureFin')      # Nouvelle heure de fin
    heure_debut = datetime.strptime(heure_debut_str, '%H:%M').time()
    heure_fin =  datetime.strptime(heure_fin_str, '%H:%M').time()

    # Récupérer les informations sur le rendez-vous existant
    with connection.cursor() as cursor:
        sql1 = "SELECT id_formateur, debut, fin FROM rdv WHERE id_rdv = %s"
        cursor.execute(sql1, (id_rdv,))
        rdv_data = cursor.fetchone()
        id_formateur = rdv_data['id_formateur']
        ancien_debut = rdv_data['debut']
        ancienne_fin = rdv_data['fin']

    nouvelle_heure_debut = datetime.combine(ancien_debut.date(), heure_debut)
    nouvelle_heure_fin = datetime.combine(ancienne_fin.date(), heure_fin)

    
    if ancien_debut == nouvelle_heure_debut and ancienne_fin == nouvelle_heure_fin:# Mettre à jour le rendez-vous existant avec les nouvelles heures de début et de fin
        with connection.cursor() as cursor:
            sql2 = "UPDATE rdv SET nom=%s, prenom=%s, email=%s,telephone=%s, debut=%s, fin=%s WHERE id_rdv=%s"
            cursor.execute(sql2, (nom,prenom,email,telephone,nouvelle_heure_debut, nouvelle_heure_fin, id_rdv))
            connection.commit()

    # Créer le rendez-vous avant (s'il y a lieu)
    elif ancien_debut == nouvelle_heure_debut and nouvelle_heure_fin < ancienne_fin :
        with connection.cursor() as cursor:
            sql3 = "UPDATE rdv SET nom=%s, prenom=%s, email=%s,telephone=%s, debut=%s, fin=%s WHERE id_rdv=%s"
            cursor.execute(sql3, (nom,prenom,email,telephone,nouvelle_heure_debut, nouvelle_heure_fin, id_rdv))
            
            sql31 = "INSERT INTO rdv (id_formateur, debut, fin) VALUES (%s, %s,%s )"
            cursor.execute(sql31, (id_formateur, nouvelle_heure_fin, ancienne_fin))
            connection.commit()

    # Créer le rendez-vous après (s'il y a lieu)
    elif nouvelle_heure_debut > ancien_debut and nouvelle_heure_fin<ancienne_fin:
        with connection.cursor() as cursor:
            sql4 = "UPDATE rdv SET nom=%s, prenom=%s, email=%s,telephone=%s, debut=%s, fin=%s WHERE id_rdv=%s"
            cursor.execute(sql4, (nom,prenom,email,telephone,nouvelle_heure_debut, nouvelle_heure_fin, id_rdv))

            sql41 = "INSERT INTO rdv (id_formateur, debut, fin) VALUES (%s, %s,%s )"
            cursor.execute(sql41, (id_formateur, nouvelle_heure_fin, ancienne_fin))
            
            sql42 = "INSERT INTO rdv (id_formateur, debut, fin) VALUES (%s, %s,%s )"
            cursor.execute(sql42, (id_formateur, ancien_debut, nouvelle_heure_debut))

            connection.commit()

    else :
         with connection.cursor() as cursor:
            sql5 = "UPDATE rdv SET nom=%s, prenom=%s, email=%s,telephone=%s, debut=%s, fin=%s WHERE id_rdv=%s"
            cursor.execute(sql5, (nom,prenom,email,telephone,nouvelle_heure_debut, nouvelle_heure_fin, id_rdv))

            sql51 = "INSERT INTO rdv (id_formateur, debut, fin) VALUES (%s, %s,%s )"
            cursor.execute(sql51, (id_formateur, ancien_debut, nouvelle_heure_debut))
            
            connection.commit()

    # Récupérer l'e-mail du formateur à partir de son ID
    with connection.cursor() as cursor:
        sql5 = "SELECT email FROM formateurs WHERE id_formateur = %s"
        cursor.execute(sql5, (id_formateur,))
        formateur_email = cursor.fetchone()['email']

    # Récupérer le nom de la formation à partir de son ID
    with connection.cursor() as cursor:
        sql6 = "SELECT nom FROM formations WHERE id_formation = %s"
        cursor.execute(sql6, (id_formation,))
        formation = cursor.fetchone()['nom']

    # Envoyer un e-mail au formateur
    msg = Message(body=f"Monsieur/Madame {nom} a pris rendez-vous avec vous à la date du {nouvelle_heure_debut}. Son numéro de téléphone est : {telephone}\nSon adresse e-mail est : {email}\n{formation}",
                  recipients=[formateur_email],
                  sender='flaskdoodle60@gmail.com', 
                  subject="rendez-vous pris")

    mail.send(msg)

    # Rediriger l'utilisateur vers une page appropriée (par exemple, la page d'accueil)
    return jsonify({'message': 'Rendez-vous enregistré avec succès !'})


@app.route('/connexion', methods=['POST'])
def connexion():
    email = request.form.get('emailConnexion')
    password = request.form.get('password')

    # Vérification des identifiants dans la base de données
    with connection.cursor() as cursor:
        sql = "SELECT id_formateur,mdp FROM formateurs WHERE email=%s"
        cursor.execute(sql, (email))
        formateur = cursor.fetchone()

    if formateur and bcrypt.checkpw(password.encode('utf-8'), formateur['mdp'].encode('utf-8')):
        # Identifiants valides, démarrer une session pour le formateur
        session['formateur_id'] = formateur['id_formateur']
        return jsonify({'success': True, 'redirect': url_for('formateur')})
    else:
        # Identifiants invalides, rediriger vers la page de connexion avec un message d'erreur
        return jsonify({'success': False, 'error': 'Identifiant ou mot de passe invalide.'})
    
@app.route('/formateur')
def formateur():
    formateur_id = session.get('formateur_id')
    
    with connection.cursor() as cursor:
        sql ="SELECT * from rdv WHERE id_formateur =%s AND nom IS NOT NULL  AND prenom is NOT NULL ORDER BY debut DESC;" 
        cursor.execute(sql,(formateur_id))
        rdv_pris = cursor.fetchall()

        sql2 ="SELECT * from rdv WHERE id_formateur =%s AND nom IS NULL AND prenom IS NULL ORDER BY debut DESC;" 
        cursor.execute(sql2,(formateur_id))
        rdv_nonpris = cursor.fetchall()

        sql3  = "SELECT * FROM formateurs WHERE id_formateur=%s"
        cursor.execute(sql3, (formateur_id,))
        formateur = cursor.fetchone()

    return render_template('formateur.jinja', formateur= formateur , rdv_pris= rdv_pris, rdv_nonpris= rdv_nonpris)

@app.route('/supprimer_rdv', methods=['POST'])
def supprimer_rdv():
    id_rdv=request.json.get('id_rdv')
    print(id_rdv)

    with connection.cursor() as cursor:
        sql="DELETE FROM rdv WHERE id_rdv=%s"    
        cursor.execute(sql,(id_rdv))

        connection.commit()

    return redirect('/')


@app.route('/deconnexion', methods=['POST'])
def deconnexion():
    # Supprimer la session de l'utilisateur
    session.pop('formateur_id', None)
    
    # Rediriger l'utilisateur vers la page d'accueil
    return redirect('/')

@app.route('/ajouterrdv', methods=['POST'])
def ajouterrdv():
    # Récupérer les données envoyées par la requête POST

# C 
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

    # Formatter les dates dans un format compatible avec MySQL
    date_debut_mysql = date_debut.strftime('%Y-%m-%d %H:%M:%S')
    date_fin_mysql = date_fin.strftime('%Y-%m-%d %H:%M:%S')

    if date_debut >= datetime.now():

        if pause == False  :  # Vérifie si aucune pause n'est spécifiée
            with connection.cursor() as cursor:
                sql = "INSERT INTO rdv (debut, fin, id_formateur) VALUES (%s, %s, %s)"
                cursor.execute(sql, (date_debut_mysql, date_fin_mysql, formateur_id))
                connection.commit()
        else:
            debutpauses = datetime.strptime(debutpause_str, "%H:%M")
            debutpause = date_debut.replace(hour=debutpauses.hour, minute=debutpauses.minute)
            dureepause_hour, dureepause_minute = map(int, dureepause_str.split(':'))
            dureepause_timedelta = timedelta(hours=dureepause_hour, minutes=dureepause_minute)
            finpause = debutpause + dureepause_timedelta
            debutpause_mysql = debutpause.strftime('%Y-%m-%d %H:%M:%S')
            finpause_mysql = finpause.strftime('%Y-%m-%d %H:%M:%S')
        
            if date_debut < debutpause or  finpause > date_fin:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO rdv (debut, fin, id_formateur) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (date_debut_mysql, debutpause_mysql, formateur_id))
                    connection.commit()

                # Insérer le deuxième rendez-vous après la pause
                with connection.cursor() as cursor:
                    sql = "INSERT INTO rdv (debut, fin, id_formateur) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (finpause_mysql, date_fin_mysql, formateur_id))
                    connection.commit()
            else : 
                return jsonify ({'error' : 'la pause ne peut pas être pris avant la date debut'})

    else :

        return jsonify ({'error' : 'la date de début ne peut être antérieur à la date actuelle'})

    # Rediriger l'utilisateur vers la page d'accueil après l'ajout du rendez-vous
    return redirect('/')





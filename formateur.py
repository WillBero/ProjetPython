from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, Blueprint
from flask_mail import Mail, Message
import pymysql.cursors
import time
import os
from dotenv import load_dotenv
import bcrypt

formateurs_bp = Blueprint('auth', __name__)


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

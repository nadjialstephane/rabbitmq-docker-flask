#!/usr/bin/python3

import requests,json,os,pika,sys

# Variables
git_url_repo="https://github.com/nadjialstephane/jeudedame/blob/master/Dame.py"
file_tache="ToDo"
taches_nbr=[]
file_resultat="Done"
resultat=0
flask_address="flask" 
rabbitmq_address="192.168.59.202"  
commit_msg="PROJETRT704"

def creationfichier(address,file):
    param = {"data" : json.dumps(file)}
    r = requests.post("http://"+address+":5000/rabbit/creation",data=param)
    print(r.text)

def envoimsg(address,tache,file):
    param = {"data" : json.dumps(tache)}
    r = requests.post("http://"+address+":5000/rabbit/envoimsg/"+file,data=param)
    print(r.text)

def msg_on(channel, method, properties, body):
    global resultat
    print (body)
    resultat_json=json.loads(body.decode())
    resultat_temp=resultat_json["Resultat"]
    resultat_id_tache=resultat_json["ID_tache"]
    taches_nbr.remove(int(resultat_id_tache))
    resultat=resultat+int(resultat_temp)

def supprimefichier(address,file):
    param = {"data" : json.dumps(file)}
    r = requests.post("http://"+address+":5000/rabbit/supprime",data=param)
    print(r.text)
    
    if len(taches_nbr)==0:
        channel.stop_consuming()
    
# Création des files
for list in file_tache,file_resultat:
    file={}
    file["file"] = list
    supprimefichier(flask_address,file)
    creationfichier(flask_address,file)
# Génération des taches
for i in range(chess_size):
    sol[0]=i
    tache={}
    tache["ID_projet"] = 1
    tache["ID_tache"] = i
    tache["URL_git"] = git_url_repo
    tache["CMD"] = "python3 /Dame.py "+str(sol).replace(" ","")
    taches_nbr.append(int(tache["ID_tache"]))
    envoi_msg(flask_address,tache,file_tache)
    
#etablir la connexion
connection = pika.BlockingConnection(pika.ConnectionParameters(host="192.168.59.202"))
channel = connection.channel()
print("En attente de message")
channel.basic_consume(file_resultat,on_msg,auto_ack=True)
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()

print("numero des solution:",resultat)

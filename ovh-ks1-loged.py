import os
import urllib.request
import json
import smtplib
import time
import datetime
from email.mime.text import MIMEText

##Variable et URL data OVH
urlovh = urllib.request.urlopen("http://www.kimsufi.com/fr/js/dedicatedAvailability/availability-data.json")
ovhdata = urlovh.read()
data = json.loads(ovhdata.decode())
datadumps=json.dumps(data, indent=4)
evaldatadumps=eval(datadumps)


##Sélection des variables dans le fichier json (185=KS1 de kimsufi.com)
ref = evaldatadumps["availability"][185]["reference"]
avail_gra = evaldatadumps["availability"][185]["zones"][0]["availability"]
avail_sbg = evaldatadumps["availability"][185]["zones"][1]["availability"]
avail_rbx = evaldatadumps["availability"][185]["zones"][2]["availability"]
avail_bhs = evaldatadumps["availability"][185]["zones"][3]["availability"]
dispo = False
while dispo == False:
	##Check si serveur sur un datacenter dispo
	if avail_gra != "unavailable":
		print ("Serveur " + ref + " dispo à Gravelines")
		currenttime = datetime.datetime.now()
		dispo = "Gravelines"
		log = open("log_KS1.txt", "a")
		log.write("Serveur " + ref + " disponible à Gravelines : " + "%s:%s:%s" % (currenttime.hour, currenttime.minute, currenttime.second) +"\n")
		log.close()
	elif avail_sbg != "unavailable":
		print ("Serveur " + ref + " dispo à Strasbourg")
		currenttime = datetime.datetime.now()
		dispo = "Strasbourg"
		log = open("log_KS1.txt", "a")
		log.write("Serveur " + ref + " disponible à Strasbourg : " + "%s:%s:%s" % (currenttime.hour, currenttime.minute, currenttime.second) +"\n")
		log.close()
	elif avail_rbx != "unavailable":
		print ("Serveur " + ref + " dispo à Roubaix")
		currenttime = datetime.datetime.now()
		dispo = "Roubaix"
		log = open("log_KS1.txt", "a")
		log.write("Serveur " + ref + " disponible à Roubaix : " + "%s:%s:%s" % (currenttime.hour, currenttime.minute, currenttime.second) +"\n")
		log.close()
	elif avail_bhs != "unavailable":
		print ("Serveur " + ref + " dispo à Beauharnois")
		currenttime = datetime.datetime.now()
		dispo = "Beauharnois"
		log = open("log_KS1.txt", "a")
		log.write("Serveur " + ref + " disponible à Beauharnois : " + "%s:%s:%s" % (currenttime.hour, currenttime.minute, currenttime.second) +"\n")
		log.close()
	else:
		print ("--------------------------------------------------\nServeur " + ref + " toujours et encore indisponible... \n\nPas d'email envoyé\n---------------------------")
		currenttime = datetime.datetime.now()
		print ("|Dernier check à : " + "%s:%s:%s" % (currenttime.hour, currenttime.minute, currenttime.second) +"|\n---------------------------")
		dispo = False
		log = open("log_KS1.txt", "a")
		log.write("Serveur " + ref + " indisponible à : " + "%s:%s:%s" % (currenttime.hour, currenttime.minute, currenttime.second) +"\n")
		log.close()
		time.sleep(10)
		currenttime = None
		
if dispo != False :
	##Création fichier txt du mail si dispo ok
		fichier = open("OVH_test.txt", "w")
		fichier.write("\n------------------------------------------------------\n\n")
		fichier.write("Le serveur OVH Référence : ")
		fichier.write(ref)
		fichier.write(" est disponible à " + dispo + " !!!\n\nPour le réserver http://www.kimsufi.com")
		fichier.write("\n\n| Dernier check à : " + "%s:%s:%s" % (currenttime.hour, currenttime.minute, currenttime.second) +" |\n")
		fichier.write("------------------------------------------------------")
		fichier.close()
		fp = open("OVH_test.txt", "r")
		msg = MIMEText(fp.read())
		fp.close()
		msg["Subject"] = "Diponibilité serveur OVH !"
		msg["From"] = "expediteur@gmail.com"
		msg["To"] = "destinataire@gmail.com"
		username = "votregmail@gmail.com"
		password = "!!!YOURPASSWORDHERE!!!"
		s = smtplib.SMTP("smtp.gmail.com:587")
		s.starttls()
		s.login(username,password)
		s.send_message(msg)
		s.quit()
		log = open("log_KS1.txt", "a")
		log.write("Serveur vu disponible à " + "%s:%s:%s" % (currenttime.hour, currenttime.minute, currenttime.second) +" pour la dernière fois\n")
		log.close()
		print ("Email envoyé à " + "%s:%s:%s" % (currenttime.hour, currenttime.minute, currenttime.second) +"|\n")
		time.sleep(60)
		dispo = False
		currenttime = None

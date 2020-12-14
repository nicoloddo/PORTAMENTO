# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 23:50:16 2020

@author: nicol
"""

from mordecai import Geoparser

import subprocess
import os
import time
ENCODING = 'utf-8'


document = "Nickelback is a Canadian rock band from Hanna, Alberta formed in 1995. Nickelback's music is classed as hard rock and alternative metal. Nickelback is one of the most commercially successful Canadian groups, having sold almost 50 million albums worldwide, ranking as the 11th best selling music act of the 2000s, and is the 2nd best selling foreign act in the U.S. behind The Beatles for the 2000's."

base_path = r'D:\PROJECTS\PORTAMENTO\ide\PORTAMENTO\PORTAMENTO'
log_file = r'output.log'

log_path = os.path.join(base_path, log_file)

print("SE NON FUNZIONA, PROVA A RIAVVIARE DOCKER")

# Creo il file di log per i subprocessi
if(not os.path.isfile(log_path)):
    log = open(log_path, "w+")
    log.close()

# Avvio il docker
with open(log_path, "a") as output:
    output.write("New session ---------------------------------------------------------------------------------\n") # Mi segno l'inizio di ogni sessione
    
    try:
        existing_containers = subprocess.check_output("docker ps -a")   # Controllo se il container esiste già
    except subprocess.CalledProcessError as e:
        print(e.output)
    
    if("geonames_index" not in existing_containers.decode(ENCODING)):    # Se non esiste già lo creo e avvio
        subprocess.call("docker run --name geonames_index -d -p 127.0.0.1:9200:9200 -v D:/Geonames/geonames_index.tar/geonames_index/:/usr/share/elasticsearch/data elasticsearch:5.5.2", shell=True, stdout=output, stderr=output)
    else:   # Se esiste lo avvio
        subprocess.call("docker start geonames_index", shell=True, stdout=output, stderr=output)

time.sleep(4)   # Spesso serve un po' più di tempo al docker per avviarsi. Questo tempo varia per ogni macchina e dipende anche dall'attuale utilizzo di CPU, dunque non può essere il giusto metodo
# Poichè lo sleep potrebbe non essere sufficiente a seconda della macchina, implementiamo un while di tentativi.
tries = 0
max_tries = 5
while True:
    tries = tries + 1
    try:
        geo = Geoparser()
    except IndexError:
        continue
    else:
        print("\nGeoparser() è andato a buon fine dopo  " + str(tries) + " tentativi\n")
        break
    if(tries == max_tries):
        print("\nGeoparser() non è andato a buon fine neanche dopo " + str(max_tries) + ". Questo era il numero massimo di tentativi consentiti: inizializzazione fallita.\n")
        break


places = geo.geoparse(document)

with open(log_path, "a") as output:
    subprocess.Popen(['docker', 'stop', 'geonames_index'], shell=True, stdout=output, stderr=output)    # Qui uso Popen perchè non aspetta che il processo termini prima di andare alla prossima istruzione
    
print(places)
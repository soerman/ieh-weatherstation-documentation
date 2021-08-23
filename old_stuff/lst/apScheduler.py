import serial
import string
import mysql
import mysql.connector
from apscheduler.schedulers.blocking import BlockingScheduler

# [Hier erfolgt die Definition der Parameter wie bereits in Abschnitt 1.1 gezeigt]

def daten():   
    try:
        #Buffer leeren
        ser.flush()
        #Befehl zum Auslesen der aktuellen Daten
        befehl = bytearray([0x02,ord('m'),ord('m'),0x03])
        ser.write(befehl)
        
	[Hier erfolgt Auslesen und Schreiben der Daten wie bereits in Abschnitt 1.1 gezeigt]
   
sched = BlockingScheduler()

# Funktion daten jede 2 Sekunden aufrufen
sched.add_job(daten, 'interval',seconds=2)

#Scheduler starten
sched.start()

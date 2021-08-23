# zur Kommunikation ueber die serielle Schnittstelle
import serial
import string
# fuer die Datenbank-Verbindung (drauf achten, dass richtige fuer Python-Version installiert)
import mysql
import mysql.connector
from time import sleep
from time import gmtime, strftime

#Parameter fuer die Verbindung zur Datenbank:
#Datenbits
bytesize=serial.EIGHTBITS
#Baudrate
baud = 115200
#Paritaet
parity = serial.PARITY_NONE
#Stopbits
stopbit = serial.STOPBITS_ONE
timeout = 5

while True:
    try:
        ser = serial.Serial('/dev/ttyUSB0',baud,bytesize,parity,stopbit,timeout)
        connection = mysql.connector.connect(host = "localhost", user = "phpmyadmin", passwd = "wetter1", db = "iehDaten")
    except Exception as e:
        print(e)  
        with open("/var/www/html/errorlog.txt", "a") as myfile:
            myfile.write(strftime("%Y-%m-%d %H:%M:%S", gmtime())+"\t"+str(e)+"\n")
        sleep(10)
    while True:
        try:
            #Buffer leeren
            ser.flush()
            #Befehl zum Auslesen der aktuellen Daten (s. Doku zur Wetterstation)
            befehl = bytearray([0x02,ord('m'),ord('m'),0x03])
            #Befehl schicken
            ser.write(befehl)
            #Auslesen der Daten
            zeile = ser.readline()
            
            print("read: "+str(zeile))
            
            #\n\r in der Zeile loeschen
            zeile = zeile.rstrip()
            # Byte-Liste in String-Liste umwandeln
            zeile = zeile.decode('utf-8')
            #Unnoetige Zeichen loeschen (entstehen durch nicht vorhandene/angeschlossene Sensoren)
            zeile = zeile.replace('---.- ----.-','')
            zeile = zeile.replace('---.-','')
            # Zeile in Daten aufteilen
            daten = zeile.split()
            
            if len(daten)<5:
                raise Exception('Read Error')
            
            #Daten in Datenbank schreiben        
            cursor = connection.cursor()
            cursor.execute("INSERT INTO wetter (windspeed,winddirection,temp,humidity,radiation,pressure,precipitation) VALUES (%s,%s,%s,%s,%s,%s,%s)"%(daten[1],daten[2],daten[3],daten[4],daten[6],daten[5],daten[7],))
            cursor.close()
            connection.commit()
                
            #eine Sekunde warten
            sleep(1)
#            print(daten)
            
           # print('Aufgetrennte Daten: '+daten)
			
			
        except Exception as e:
            print(e)
            with open("/var/www/html/errorlog.txt", "a") as myfile:
                myfile.write(strftime("%Y-%m-%d %H:%M:%S", gmtime())+"\t"+str(e)+"\n")
                sleep(10)
        
        

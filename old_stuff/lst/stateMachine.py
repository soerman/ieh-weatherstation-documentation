import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import os
from fysom import *




continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# State Machine
fsm = Fysom({'initial' : 'nobodyAtHome', 'final' : 'red', 'events': [{'name': 'comingHome', 'src': 'nobodyAtHome', 'dst': 'somebodyAtHome'}, {'name': 'leavingHome', 'src' : 'somebodyAtHome', 'dst': 'nobodyAtHome'}]})
temp = False

while continue_reading:
	
	(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
	
	if status == MIFAREReader.MI_OK and temp != True: 
		temp = True
		fsm.comingHome()
		print(fsm.current)
		os.system('/usr/bin/curl -s --header "Content-Type: text/plain" --request POST --data "ON" http://localhost:8080/rest/items/RFID_Status')
		time.sleep(10)
		
	if status == MIFAREReader.MI_OK and temp == True:
		temp = False
		fsm.leavingHome()
		print(fsm.current)
		os.system('/usr/bin/curl -s --header "Content-Type: text/plain" --request POST --data "OFF" http://localhost:8080/rest/items/RFID_Status')
		time.sleep(3)
		
		
		#http://rpi.ddnss.org:8080/rest/items/RFID_Status


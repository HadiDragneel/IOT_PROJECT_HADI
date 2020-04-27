#Hadi Sadeghi
#INF2E
#PIR Motion Sensor Security

import RPi.GPIO as GPIO
import time
import datetime
from datetime import datetime
import http.client, urllib
import requests
import os



#BCM mode to identify GPIO using their numbers not pin numbers.
GPIO.setmode(GPIO.BCM)
#The GPIO number used to plug in the PIR Motion Sensor.
PIR_PIN = 21
#Setup for the PIR mosion sensor.
GPIO.setup(PIR_PIN, GPIO.IN)
#Goes up when someone is detected. Only sends notification on the value of 1 to avoid spam.
D = 0
#Used to identify a motion/intruder as a number for Thingspeak.
IntruderNumber = 0               
    
    
def UpdateThingspeak(): # Uses Thingspeak API to update the graph containing intruder data.
    RequestToThingspeak = 'https://api.thingspeak.com/update?api_key=ZAMUY1JDKUJT882A&field1='
    RequestToThingspeak += str(IntruderNumber)
    request = requests.get(RequestToThingspeak)
    print('Data uploaded to Thingspeak.')
    
    
def SendNotificationNew(): # Uses a bash script which uses the Pushbullet API to send a notification to my phone.
    os.system('/home/pi/pushbullet.sh "Movement detected! Be careful."')
    

def PlayWarningSound(): # Plays a custom sound file I recorded warning the intruders that I am aware of their presense.
    os.system("omxplayer -o local warning.aac")

                       

try:
    print("PIR Motion Sensor is starting...")
    time.sleep(60)              #The PIR Motion Sensor works better after being warmed up for 60 seconds.                                    
    print ("Sensor is ready to go. Scanning started...")
    while True:                 #Infinite loop to scan until stopped manually by the user.
        input = GPIO.input(PIR_PIN)
        now = datetime.now()
        Current_Time = now.strftime("%H:%M:%S")
        if input == 0:          #If no input is given from sensor, the program waits 1 seconds and repeats the loop.
            D = 0
            time.sleep(1)
        if input == 1:
            print ("Motion Detected! Intruder spotted at: " + Current_Time)
            D += 1
            if D == 1:          #This prevents spamming. D goes up with signals from PIR Sensor and notifies user 1 time per movement.
                IntruderNumber += 1
                PlayWarningSound()
                UpdateThingspeak()
                SendNotificationNew()
#                 SendNotificationOld()
                time.sleep(5)
            time.sleep(5)
  
      
except KeyboardInterrupt:
               print ("Scanning cancelled.")
               GPIO.cleanup()  #Proper closing of the program when interrupted manually.
               
               
               
               
               
# Old notification service using Pushover. More info regarding this topic in the documentation.

               
def SendNotificationOld(): #Uses Pushbullet API to send high priority notification to phone. This notification will always make a sound at max volume.
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.parse.urlencode({
        "token": "az8t98qpnimu9uqz5g9nu9v3gb36sz",
        "user": "ui3p2afyxk6148471h9m2c3bxbg1uv",
        "message": "Someone was spotted at your door. Be careful!",
        "title": "Intruder Alert",
        "priority": "1",
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
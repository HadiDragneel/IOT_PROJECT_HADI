#Hadi Sadeghi
#INF2E
#PIR Motion Sensor Security

import RPi.GPIO as GPIO
import time
import datetime
import os
from datetime import datetime
import http.client, urllib
import requests


GPIO.setmode(GPIO.BCM)       #BCM mode to identify GPIO using their numbers not pin numbers
PIR_PIN = 21                 #The GPIO number used to plug in the PIR Motion Sensor
GPIO.setup(PIR_PIN, GPIO.IN) #Setup for the PIR mosion sensor.
D = 0                        #Goes up when someone is detected. Only sends notification on the value of 1 to avoid spam.
IntruderID = 0


def NotifyUser(): #Sends high priority urgent notification to the user specified. This notification will make sound even when th phone is put on silent.
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
    
    
def UpdateThingspeak():
    RequestToThingspeak = 'https://api.thingspeak.com/update?api_key=8KL4YUMHRSYF8OPH&field1='
    RequestToThingspeak += str(IntruderID)
    request = requests.get(RequestToThingspeak)
    print('Data uploaded to Thingspeak.')


try:
    print("PIR Motion Sensor is starting...")
    time.sleep(10) #The PIR Motion Sensor works better after being warmed up for 60 seconds.                                    
    print ("Sensor is ready to go. Scanning started...")
    while True:
        input = GPIO.input(PIR_PIN)
        now = datetime.now()
        Current_Time = now.strftime("%H:%M:%S")
        if input == 0:
            D = 0
            time.sleep(1)
        if input == 1:
            print ("Motion Detected! Intruder spotted at: " + Current_Time)
            D = D + 1
            if D == 1:
                NotifyUser()
                IntruderID = IntruderID + 1
                UpdateThingspeak()
                time.sleep(5)
            time.sleep(1)
  
      
except KeyboardInterrupt:
               print ("Scanning cancelled.")
               GPIO.cleanup()
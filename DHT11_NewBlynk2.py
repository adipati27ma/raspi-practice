"""
This Code is belong to SME Dehraun. for any query write to schematicslab@gmail.com

"""
import sys
 
# adding blynk-library-python to the system path
sys.path.insert(0, '/home/pi/blynk-library-python')


import BlynkLib
import RPi.GPIO as GPIO
from BlynkTimer import BlynkTimer

import Adafruit_DHT
import time

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 26
BLYNK_AUTH_TOKEN = '6fRGgiZx_HjIumonIflCb6dzZK00xm0e'

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

# Create BlynkTimer Instance
timer = BlynkTimer()


# function to sync the data from virtual pins
@blynk.on("connected")
def blynk_connected():
    print("Hi, You have Connected to New Blynk2.0")
    print(".......................................................")
    print("................... By SME Dehradun ...................")
    time.sleep(2);

# Functon for collect data from sensor & send it to Server
def myData():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Sensor failure. Check wiring.");

    blynk.virtual_write(0, humidity,)
    blynk.virtual_write(1, temperature)
    print("Values sent to New Blynk Server!")

timer.set_interval(2, myData)


while True:
    blynk.run()
    timer.run()
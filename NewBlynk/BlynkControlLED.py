"""
This code i Belogs to SME Dehradun Firm. For any query, mail us at schematicslab@gmail.com 
"""

import BlynkLib
import RPi.GPIO as GPIO
from BlynkTimer import BlynkTimer

BLYNK_AUTH_TOKEN = '37x03F1Nd3smnD5BmQamusfrBab3kftT'

led1 = 22
led2 = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

# Led control through V0 virtual pin
@blynk.on("V0")
def v0_write_handler(value):
#    global led_switch
    if int(value[0]) is not 0:
        GPIO.output(led1, GPIO.HIGH)
        print('LED1 HIGH')
    else:
        GPIO.output(led1, GPIO.LOW)
        print('LED1 LOW')

# Led control through V0 virtual pin
@blynk.on("V1")
def v1_write_handler(value):
#    global led_switch
    if int(value[0]) is not 0:
        GPIO.output(led2, GPIO.HIGH)
        print('LED2 HIGH')
    else:
        GPIO.output(led2, GPIO.LOW)
        print('LED2 LOW')

#function to sync the data from virtual pins
@blynk.on("connected")
def blynk_connected():
    print("Raspberry Pi Connected to New Blynk") 

while True:
    blynk.run()
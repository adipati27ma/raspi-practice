"""
This code i Belogs to SME Dehradun Firm. For any query, mail us at schematicslab@gmail.com 
"""

import BlynkLib
import RPi.GPIO as GPIO
from BlynkTimer import BlynkTimer
import time

BLYNK_AUTH_TOKEN = '37x03F1Nd3smnD5BmQamusfrBab3kftT'

led1 = 22
led2 = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

# Create BlynkTimer Instance
timer = BlynkTimer()

# define custom function
def myData():
    data1 = 1
    data2 = 2

    blynk.virtual_write(2, data1 + 1)
    blynk.virtual_write(3, data2 + 1)
    print("Values sent to New Blynk Server!")

# Led control through V0 virtual pin
@blynk.on("V0")
def v0_write_handler(value):
#    global led_switch
    if int(value[0]) is not 0:
        GPIO.output(led1, GPIO.HIGH)
        blynk.virtual_write(2, 1)
        print('LED1 HIGH')
    else:
        GPIO.output(led1, GPIO.LOW)
        blynk.virtual_write(2, 0)
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
    time.sleep(2);


timer.set_interval(2, myData)

while True:
    blynk.run()
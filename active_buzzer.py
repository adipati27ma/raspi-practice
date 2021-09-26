#              .';:cc;.
#            .,',;lol::c.
#            ;';lddddlclo
#            lcloxxoddodxdool:,.
#            cxdddxdodxdkOkkkkkkkd:.
#          .ldxkkOOOOkkOO000Okkxkkkkx:.
#        .lddxkkOkOOO0OOO0000Okxxxxkkkk:
#       'ooddkkkxxkO0000KK00Okxdoodxkkkko
#      .ooodxkkxxxOO000kkkO0KOxolooxkkxxkl
#      lolodxkkxxkOx,.      .lkdolodkkxxxO.
#      doloodxkkkOk           ....   .,cxO;
#      ddoodddxkkkk:         ,oxxxkOdc'..o'
#      :kdddxxxxd,  ,lolccldxxxkkOOOkkkko,
#       lOkxkkk;  :xkkkkkkkkOOO000OOkkOOk.
#        ;00Ok' 'O000OO0000000000OOOO0Od.
#         .l0l.;OOO000000OOOOOO000000x,
#            .'OKKKK00000000000000kc.
#               .:ox0KKKKKKK0kdc,.
#                      ...
#
# Author: peppe8o
# Date: Sep 20th, 2020
# Version: 1.0
#
# website: https://peppe8o.com

# Import required libraries
import sys
import RPi.GPIO as GPIO
import time

# Set trigger PIN according with your cabling
signalPIN = 17

# Set PIN to output
GPIO.setmode(GPIO.BCM)
GPIO.setup(signalPIN,GPIO.OUT)

# this row makes buzzer work for 1 second, then
# cleanup will free PINS and exit will terminate code execution

for x in range(10) :
	GPIO.output(signalPIN,1)
	time.sleep(1)
	GPIO.output(signalPIN,0)
	time.sleep(0.5)

time.sleep(1)
GPIO.cleanup()
sys.exit()


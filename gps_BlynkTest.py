import BlynkLib
from gps import *
from gpiozero import LED, TonalBuzzer
from gpiozero.tones import Tone
from datetime import datetime
from time import sleep
import RPi.GPIO as GPIO

# Initialize Blynk & State for GPS
blynk = BlynkLib.Blynk('1EWSq_x7ATOX7ejvCMx5OwNVF9RtOFIe')
running = True

# Initialize GPIO
led = LED(17)
#buzzer = TonalBuzzer(27)
triggerPIN = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(triggerPIN, GPIO.OUT)
buzzer = GPIO.PWM(triggerPIN, 4000)

# GPS Function
def getPositionData(gps):
  nx = gpsd.next()
	
  # For a list of all supported classes and fields refer to:
  # https://gpsd.gitlab.io/gpsd/gpsd_json.html
  if nx['class'] == 'TPV':
    latitude = getattr(nx,'lat', "Unknown")
    longitude = getattr(nx,'lon', "Unknown")
    print("Your position: lon = " + str(longitude) + ", lat = " + str(latitude))



# Register Virtual Pin
@blynk.VIRTUAL_READ(2)
def my_read_handler():
  currentTime = datetime.now()
  blynk.virtual_write(2, currentTime.strftime("%d/%m/%Y %H:%M:%S"))

@blynk.VIRTUAL_WRITE(1)
def my_write_handler(value):
	gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
	
	if int(value[0]) == 1:
		led.on()
		#buzzer.play("F5")
		buzzer.start(10)
		blynk.virtual_write(0, 255)
		blynk.virtual_write(5, 1, 51.5074, 0.1278, "value")
		#sleep(5)
		#blynk.notify('Pengemudi mulai mengantuk!!')
		getPositionData(gpsd)
		sleep(1)
	else:
		led.off()
		buzzer.stop()
		blynk.virtual_write(0, 0)
	print('Current V1 value: {}'.format(value[0]))

print("started!")
while True:
    blynk.run()

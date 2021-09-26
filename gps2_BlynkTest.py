import BlynkLib
from gps import *
# from gpiozero import LED
from datetime import datetime
from time import sleep
# import RPi.GPIO as GPIO

# Initialize Blynk & State for GPS
blynk = BlynkLib.Blynk('1EWSq_x7ATOX7ejvCMx5OwNVF9RtOFIe')
sendingData = False

# Initialize GPIO
# led = LED(17)
# triggerPIN = 13
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(triggerPIN, GPIO.OUT)

# GPS Function
def getPositionData(gps):
  nx = gps.next()
	
  # For a list of all supported classes and fields refer to:
  # https://gpsd.gitlab.io/gpsd/gpsd_json.html
  if nx['class'] == 'TPV':
    latitude = getattr(nx,'lat', "Unknown")
    longitude = getattr(nx,'lon', "Unknown")
    positionData = [latitude, longitude]

    return positionData



# Register Virtual Pin
# @blynk.VIRTUAL_READ(2)
# def my_read_handler():
#   currentTime = datetime.now()
#   blynk.virtual_write(2, currentTime.strftime("%d/%m/%Y %H:%M:%S"))

@blynk.VIRTUAL_WRITE(1)
def my_write_handler(value) :
  global sendingData
  intValue = int(value[0])
  print(intValue)
  if sendingData :
    blynk.virtual_write(1, 1)
    return
  if intValue == 0 : return

  gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
  print("Sending data...")
  sendingData = True

  for x in range(10) :
    dataGps = getPositionData(gpsd)
    print(dataGps)
    if dataGps :
      blynk.virtual_write(5, 1, dataGps[0], dataGps[1], "value")
      blynk.virtual_write(2, str(dataGps))
    time.sleep(0.5)
  
  blynk.virtual_write(1, 0)
  sendingData = False
  print("Data transfer stopped.")

  # while running:
  #   dataGps = getPositionData(gpsd)
  #   blynk.virtual_write(5, 1, dataGps[0], dataGps[1], "value")
  #   # print(dataGps)
  #   time.sleep(1.0)
	
  #   if int(value) == 1:
  #     pass
  #   else:
  #     running = False

print("started!")
while True:
    blynk.run()
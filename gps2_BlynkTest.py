import BlynkLib
from subprocess import check_output
from gps import *
# from gpiozero import LED
import time
# import RPi.GPIO as GPIO
import threading

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


def sendPositionData(gpsd):
  global sendingData
  
  start = time.perf_counter() # for response time debugging
  for x in range(10) :
    if x == 4: finish = time.perf_counter() # for response time debugging
    
    dataGps = getPositionData(gpsd)
    print(dataGps)
    if dataGps :
      blynk.virtual_write(5, 1, dataGps[0], dataGps[1], "value")
      blynk.virtual_write(2, str(dataGps))
    time.sleep(0.2)
  
  blynk.virtual_write(1, 0)
  sendingData = False
  print("Data transfer stopped.")
  print(f'Finished in {round(finish-start, 5)} second(s)') # for response time debugging



@blynk.VIRTUAL_WRITE(1)
def my_write_handler(value) :
  global sendingData
  intValue = int(value[0])
  if sendingData :
    blynk.virtual_write(1, 1)
    return
  if intValue == 0 : return

  gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
  print("Sending data...")
  sendingData = True

  sendThread = threading.Thread(target=sendPositionData, args=[gpsd])
  sendThread.start()



wifi_ip = check_output(['hostname', '-I'])
if (wifi_ip is not None):
  print("Connected")
  print("started!")
  while True:
    blynk.run()
else:
  print("Not Connected")
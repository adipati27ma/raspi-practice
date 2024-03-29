import BlynkLib
from Adafruit_IO import *
from gps import *
from subprocess import check_output
# from gpiozero import LED
import time
# import RPi.GPIO as GPIO
import threading

# Initialize Blynk, Adafruit IO, & State for GPS
blynk = BlynkLib.Blynk('1EWSq_x7ATOX7ejvCMx5OwNVF9RtOFIe')
aio = Client('adipati27ma', 'aio_TdlI51n0cWNXf86l7gioLg9iz2T1')
sendingData = False
sentAdafruit = False

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

# Function sendToBlynk & sendToAdafruit
def sendToBlynk(dataGps):
  blynk.virtual_write(5, 1, dataGps[0], dataGps[1], "value")
  blynk.virtual_write(2, str(dataGps))

def sendToAdafruit(dataLevel, metaData):
  aio.send("sleepy-driver-data-history", dataLevel, metaData)


# Function send Pos Data
def sendPositionData(gpsd):
  global sendingData
  global sentAdafruit
  dataLevel = 1
  
  start = time.perf_counter() # for response time debugging
  for x in range(10) :
    if x == 5: finish = time.perf_counter() # for response time debugging
    
    dataGps = getPositionData(gpsd)
    print(dataGps)
    if dataGps :
      metaData = {
        'lat': dataGps[0],
        'lon': dataGps[1],
        'ele': 0,
        'created_at': None,
      }
      
      sendBlynk = threading.Thread(target=sendToBlynk, args=[dataGps])
      sendBlynk.start()
      if (sentAdafruit == False):
        sendAdafruit = threading.Thread(target=sendToAdafruit, args=[dataLevel, metaData])
        sendAdafruit.start()
        sentAdafruit = True
    time.sleep(0.2)
  
  blynk.virtual_write(1, 0)
  sendingData = False
  sentAdafruit = False
  finishAll = time.perf_counter()
  print("Data transfer stopped.")
  print(f'Finished in {round(finish-start, 5)} second(s)') # for response time debugging
  print(f'Finished ALL in {round(finishAll-start, 5)} second(s)') # for response time debugging


# Input from Blynk (will send data gps to Blynk)
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
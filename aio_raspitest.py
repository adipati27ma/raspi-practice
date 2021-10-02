from Adafruit_IO import *


aio = Client('adipati27ma', 'aio_VWIo953Vo35Ko5ktrlCPOpDaIP8x')
metadata = {
  'lat': -6.947038,
  'lon': 107.661577,
  'ele': 0,
  'created_at': None,
}
data = "Hello, I'm in position"

aio.send("raspi-test1", data, metadata)
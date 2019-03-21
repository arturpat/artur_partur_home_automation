import sys

import Adafruit_DHT
from datetime import datetime, date
from time import sleep
from ADConverter import AnalogDigitalProxy

humidity = None  # type: float
temperature = None  # type: float
light = None  # type: int
ad_proxy = AnalogDigitalProxy(channel=0)

fname = str(date.today()) + '.csv'
with open(fname, 'w') as fd:
    fd.write("Datetime,temperature,humidity,light_reading\n")

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)  # DHT11, pin 18 (GPIO4)
    if not humidity:
        humidity = 0
    if not temperature:
        temperature = 0

    light = 255 - ad_proxy.get_readings()
    line = "{},{},{},{}\n".format(datetime.now().isoformat(), temperature, humidity, light)
    # print(line, end='')
    print('Temp: {0:0.1f} C  Humidity: {1:0.1f}% Light: {2}'.format(temperature, humidity, light))

    with open(fname, 'a') as fd:
        fd.write(line)
    for i in range(5):
        sys.stdout.flush()
        sys.stdout.write('.')
        sleep(10)
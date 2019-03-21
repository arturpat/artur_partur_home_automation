import Adafruit_DHT
from datetime import datetime, date
from time import sleep
from ADconverter import AnalogDigitalProxy

humidity = None  # type: float
temperature = None  # type: float
light = None  # type: int
ad_proxy = AnalogDigitalProxy(channel=0)

fname = str(date.today()) + '.csv'
with open(fname, 'w') as fd:
    fd.write("Datetime,temperature,humidity,light_reading\n")

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)  # DHT11, pin 18 (GPIO4)
    light = ad_proxy.get_readings()
    line = "{},{},{},{}\n".format(datetime.now().isoformat(), temperature, humidity, light)
    print(line, end='')
    sleep(30)

    # with open(fname, 'a') as fd:
    #     fd.write(line)
    # for i in range(5):
    #     sys.stdout.flush()
    #     sys.stdout.write('.')
    #     sleep(60)
    # print()

    print('Temp: {0:0.1f} C  Humidity: {1:0.1f} Light: {}%'.format(temperature, humidity, light))



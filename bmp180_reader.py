from typing import List

import Adafruit_BMP.BMP085 as BMP085
from time import sleep


class BmpSensorProxy(object):
    def __init__(self):
        self.bmp_sensor = BMP085.BMP085()

    def get_temp(self) -> float:
        try:
            return self.bmp_sensor.read_temperature()
        except OSError:
            return -1

    def get_pressure(self) -> float:
        try:
            return self.bmp_sensor.read_pressure()
        except OSError:
            return -1

    def read_all(self) -> List:
        return ['Temp = {0:0.2f} *C'.format(self.bmp_sensor.read_temperature()),  # Temperature in Celcius
                'Pressure = {0:0.2f} Pa'.format(self.bmp_sensor.read_pressure()),  # The local pressure
                'Altitude = {0:0.2f} m'.format(self.bmp_sensor.read_altitude()),  # The current altitude
                # The sea-level pressure
                'Sealevel Pressure = {0:0.2f} Pa'.format(self.bmp_sensor.read_sealevel_pressure())]


if __name__ == "__main__":
    bmp_sensor = BmpSensorProxy()
    while True:
        print(bmp_sensor.read_all())
        sleep(1)

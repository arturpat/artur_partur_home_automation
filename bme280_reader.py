from time import sleep
from typing import Dict, Any

import smbus2
import bme280


class Bme280SensorProxy(object):
    def __init__(self, address: hex = 0x76):
        self.port = 1
        self.address = address
        self.bus = smbus2.SMBus(self.port)
        self.calibration_params = bme280.load_calibration_params(self.bus, address)
        self.temp = 0.0
        self.pressure = 0.0
        self.humidity = 0.0
        self.data_string = ""

    def __repr__(self):
        return self.data_string

    def sample_sensor(self):
        """
        the sample method will take a single reading and return a
        compensated_reading object
        :return:
        """
        try:
            sampled_data = bme280.sample(self.bus, self.address, self.calibration_params)
            self.temp = sampled_data.temperature
            self.pressure = sampled_data.pressure
            self.humidity = sampled_data.humidity
            self.data_string = str(sampled_data)
        except OSError:
            self.temp = -1
            self.pressure = -1
            self.humidity = -1

    def get_temp(self) -> float:
        self.sample_sensor()
        return self.temp

    def get_pressure(self) -> float:
        self.sample_sensor()
        return self.pressure

    def get_humidity(self) -> float:
        self.sample_sensor()
        return self.humidity

    def get_all(self) -> Dict[str, Any]:
        self.sample_sensor()
        return {
            "humidity": self.humidity,
            "temperature": self.temp,
            "pressure": self.pressure}


if __name__ == "__main__":
    sensor = Bme280SensorProxy()
    while True:
        sensor.sample_sensor()
        print(sensor)
        sleep(1)

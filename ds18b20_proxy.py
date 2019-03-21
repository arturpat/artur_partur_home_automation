import os
from time import sleep


class ds18b20Proxy(object):
    def __init__(self):
        for i in os.listdir('/sys/bus/w1/devices'):
            if i != 'w1_bus_master1':
                self.sensor = i
                break
        else:
            raise FileNotFoundError("Sensor seems offline")

    def get_temp(self):
        location = '/sys/bus/w1/devices/' + self.sensor + '/w1_slave'
        tfile = open(location)
        text = tfile.read()
        tfile.close()
        secondline = text.split("\n")[1]
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:])
        celsius = float('{0:0.2f}'.format(temperature / 1000))
        return celsius


if __name__ == '__main__':
    sensor = ds18b20Proxy()
    while True:
        print(sensor.get_temp())
        sleep(1)

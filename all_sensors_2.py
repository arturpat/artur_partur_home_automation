import sys
import os
from datetime import datetime, date
from time import sleep
from ADconverter import AnalogDigitalProxy
from bmp180_reader import BmpSensorProxy
from display_proxy import DisplayProxy
from ds18b20_proxy import ds18b20Proxy


class SensorWatcher(object):
    def __init__(self):
        self.temperature_bmp = None  # type: float
        self.temperature_probe = None  # type: float
        self.light = None  # type: int
        self.pressure = None  # type: int
        self.ad_proxy = AnalogDigitalProxy(channel=0)
        self.bmp_proxy = BmpSensorProxy()
        self.display_proxy = DisplayProxy()
        self.temp_probe_proxy = ds18b20Proxy()

        try:
            os.mkdir('logs')
        except FileExistsError:
            print("Logs dir exists, continuing...")
        self.fname = os.path.join('logs', str(date.today()) + '_v2.csv')
        with open(self.fname, 'w') as fd:
            fd.write("Datetime,temperature_bmp,temperature_probe,pressure,light_reading\n")

    def update_readings(self):
        self.temperature_bmp = self.bmp_proxy.get_temp()
        self.pressure = self.bmp_proxy.get_pressure()
        self.light = 255 - self.ad_proxy.get_readings()
        self.temperature_probe = self.temp_probe_proxy.get_temp()

    def append_current_results_to_csv(self):
        line = "{},{},{},{},{}\n".format(datetime.now().isoformat(), self.temperature_bmp, self.temperature_probe,
                                         self.pressure, self.light)
        with open(self.fname, 'a') as fd:
            fd.write(line)

        print('File updated: Temp_bmp: {0:0.1f} C  Temp_probe: {1:0.1f} Pressure: {2} Pa Light: {3}'
              .format(self.temperature_bmp, self.temperature_probe, self.pressure, self.light))

    def display_current_results_on_lcd(self):
        self.display_proxy.display_text_lines(["Temp bmp: {} C".format(self.temperature_bmp),
                                               "Temp probe: {} C".format(self.temperature_probe),
                                               "Pressure: {} Pa".format(self.pressure),
                                               "Light: {}".format(self.light)])


if __name__ == "__main__":
    sensor_watcher = SensorWatcher()
    logging_interval_secs = 20
    last_csv_writing_time = datetime.now()
    while True:
        sensor_watcher.update_readings()
        reading_time = datetime.now()
        sensor_watcher.display_current_results_on_lcd()
        sys.stdout.flush()
        sys.stdout.write('.')
        sleep(1)
        if (reading_time - last_csv_writing_time).seconds > logging_interval_secs:
            sensor_watcher.append_current_results_to_csv()
            last_csv_writing_time = datetime.now()

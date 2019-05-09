import bmp280

sensor = bmp280.BMP280(i2c_addr=0x76)
print('pressure: ' + sensor.get_pressure())
print('temp: ' + sensor.temperature)

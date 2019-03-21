import smbus
import time


# SDA1, SCL1 on the expansion board
# GND and VCC given is at the same time high sign level, so VCC should go to +3V

class AnalogDigitalProxy(object):
    def __init__(self, channel: int, dev_addr: hex = 0x48) -> None:
        """
        Creates an object to read from a given channel from a device with dev_addr where channels are
        (If all jumpers are on):
        0 is photocell
        1 is termister
        2 is Analog In 2
        3 is knob resistor
        :param dev_addr:
        """
        self.channel = channel
        self.dev_addr = dev_addr
        self._bus = smbus.SMBus(1)
        self.change_channel(channel)

    def change_channel(self, channel):
        self._bus.write_byte(self.dev_addr, channel)

    def get_readings(self) -> int:
        """
        Gets readings from the channel.
        :return: value 0 - 255
        """
        try:
            return int(self._bus.read_byte(self.dev_addr))
        except OSError:
            return -1


if __name__ == '__main__':
    ad_c = AnalogDigitalProxy(channel=0)
    while True:
        print(ad_c.get_readings())
        time.sleep(1)

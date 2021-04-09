from . import Sensor


class PowerSwitch(Sensor):
    """Class representing a power switch."""

    def __init__(self, data, panel):
        super().__init__(data, panel)

        self._onOff = int(data.get('onOff'))  # Power switches only
        self._always_off = int(data.get('always_off'))  # Power switches only

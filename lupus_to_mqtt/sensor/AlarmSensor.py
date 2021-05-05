from . import Sensor


class AlarmSensor(Sensor):
    """Class representing a currently unsupported sensor. Only used to read for alarm statuses."""

    def registerDevice(self):
        pass

    def sendUpdate(self):
        pass

    def __init__(self, data, panel):
        super().__init__(data, panel)
        self._alarm_status = data.get('alarm_status')

    def updateFromData(self, data):
        new_alarm_status = data.get('alarm_status')

        if self._alarm_status != new_alarm_status:
            updated = True
        else:
            updated = False

        self._alarm_status = new_alarm_status

        return updated

    @property
    def alarmStatus(self):
        return self._alarm_status

    def isBurglarAlarm(self):
        return self._alarm_status == 'BURGLAR'

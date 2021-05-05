import json

from lupus_to_mqtt.MQTT import MQTT
from . import AlarmSensor


class DoorWindowSensor(AlarmSensor.AlarmSensor):
    """Class representing a door/window switch."""

    def __init__(self, data, panel):
        self._openClose = int(data.get('openClose'))  # Binary sensors only

        super().__init__(data, panel)

    def registerDevice(self):
        mqtt = MQTT.getInstance()
        msg_config = json.dumps({
            "name": self.name,
            "unique_id": self._id,
            "availability_topic": self._panel.device_name + "/availability",
            "state_topic": f'{self._panel.device_name}/{self._id}/state',
            "device": {
                "identifiers": self._sid,
                "manufacturer": self._panel.manufacturer,
                "name": self.name,
            }
        }
        )
        mqtt.publish_message(f'homeassistant/binary_sensor/{self._id}/config', msg_config)
        self.sendUpdate()

    def updateFromData(self, data):
        newOpenClose = int(data.get('openClose'))

        updated = super().updateFromData(data)

        if self._openClose != newOpenClose:
            updated = True

        self._openClose = newOpenClose  # Binary sensors only

        return updated

    def sendUpdate(self):
        mqtt = MQTT.getInstance()
        mqtt.publish_message(f'{self._panel.device_name}/{self._id}/state', ('OFF', 'ON')[self._openClose])

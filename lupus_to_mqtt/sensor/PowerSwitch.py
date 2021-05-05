import json

from lupus_to_mqtt.MQTT import MQTT
from lupus_to_mqtt.Logger import Logger
from lupus_to_mqtt.Connection import Connection
from . import Sensor


class PowerSwitch(Sensor):
    """Class representing a power switch."""

    def __init__(self, data, panel):
        super().__init__(data, panel)

        self._onOff = int(data.get('onOff'))  # Power switches only
        self._always_off = int(data.get('always_off'))  # Power switches only
        self._logger = Logger.getInstance()
        self._connection = Connection.getInstance()

    def registerDevice(self):
        mqtt = MQTT.getInstance()
        msg_config = json.dumps({
            "name": self.name,
            "unique_id": self._id,
            "availability_topic": self._panel.device_name + "/availability",
            "state_topic": f'{self._panel.device_name}/{self._id}/state',
            "command_topic": f'{self._panel.device_name}/{self._id}/set',
            "device": {
                "identifiers": self._sid,
                "manufacturer": self._panel.manufacturer,
                "name": self.name,
            }
        }
        )
        mqtt.publish_message(f'homeassistant/switch/{self._id}/config', msg_config)
        mqtt.client.subscribe(f'{self._panel.device_name}/{self._id}/set', 0)
        self.sendUpdate()

    def updateFromData(self, data):
        newOnOff = int(data.get('onOff'))
        newAlwaysOff = int(data.get('always_off'))

        updated = super().updateFromData(data)

        if self._onOff != newOnOff or self._always_off != newAlwaysOff:
            updated = True

        self._onOff = newOnOff  # Binary sensors only
        self._openClose = newAlwaysOff  # Binary sensors only

        return updated

    def sendUpdate(self):
        mqtt = MQTT.getInstance()
        mqtt.publish_message(f'{self._panel.device_name}/{self._id}/state', ('OFF', 'ON')[self._onOff])

    def onMessage(self, client, userdata, message, msg_data):
        if message.topic == f'{self._panel.device_name}/{self._id}/set':
            if msg_data == 'ON':
                self._connection.post('haExecutePost', {'exec': f'a={self._area}&z={self._zone}&sw=on'})
            elif msg_data == 'OFF':
                self._connection.post('haExecutePost', {'exec': f'a={self._area}&z={self._zone}&sw=off'})

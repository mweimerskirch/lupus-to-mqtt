import json

from lupus_to_mqtt import constants as CONST
from lupus_to_mqtt.Connection import Connection
from lupus_to_mqtt.Logger import Logger
from lupus_to_mqtt.MQTT import MQTT
from lupus_to_mqtt.sensor.AlarmSensor import AlarmSensor
from lupus_to_mqtt.sensor.DoorWindowSensor import DoorWindowSensor
from lupus_to_mqtt.sensor.PowerSwitch import PowerSwitch


class Panel:
    """Class representing an alarm device."""

    def __init__(self, device_name, host, username, password, manufacturer, model, alarm_statuses, verify_ssl):
        self._device_name = device_name
        self._mqtt = MQTT.getInstance()
        self._logger = Logger.getInstance()
        self._connection = Connection(host, username, password, verify_ssl)
        self._mode = CONST.MODE_DISARM
        self._sensors = {}
        self._manufacturer = manufacturer
        self._model = model

        # List of current alarm statuses
        self._alarm_statuses = {}
        for alarm_status in alarm_statuses:
            alarm_status = alarm_status.strip()
            if alarm_status in CONST.SUPPORTED_ALARM_STATUSES:
                self._alarm_statuses[alarm_status] = 'OFF'
            else:
                self._logger.logWarning(f'Alarm status {alarm_status} not supported, so no sensor is being created for it.')

    def setupMQTTAlarmControlPanel(self):
        version = self.get_version()
        msg_config = json.dumps({
            "name": self._device_name,
            "unique_id": self._device_name,
            "availability_topic": self._device_name + "/availability",
            "command_topic": self._device_name + "/command",
            "state_topic": self._device_name + "/state",
            "code_arm_required": False,
            "code_disarm_required": False,
            "device": {
                "identifiers": self._device_name,
                "manufacturer": self._manufacturer,
                "model": self._model,
                "name": self._device_name,
                "sw_version": version
            }
        }
        )
        self._mqtt.publish_message("homeassistant/alarm_control_panel/" + self._device_name + "/config", msg_config)
        self._mqtt.client.subscribe(self._device_name + "/command", 0)

    def setupMQTTAlarmSensors(self, alarm_status: str):
        """Create MQTT binary sensors for each configured alarm state (e.g. "burglar", "doorbell", etc)"""
        alarm_status_lower = alarm_status.lower()
        msg_config = json.dumps({
            "name": f'{self._device_name}_{alarm_status_lower}',
            "unique_id": f'{self._device_name}_{alarm_status_lower}',
            "availability_topic": self._device_name + "/availability",
            "state_topic": f'{self._device_name}/{alarm_status_lower}_state',
            "device": {
                "identifiers": f'{self._device_name}_{alarm_status_lower}',
                "manufacturer": self._manufacturer,
                "model": self._model,
            }
        }
        )
        self._mqtt.publish_message(f'homeassistant/binary_sensor/{self._device_name}_{alarm_status_lower}/config', msg_config)

    def on_connect(self, client, userdata, flags, rc):
        """MQTT connection callback: Register the devices."""
        self._mqtt.publish_message(self._device_name + "/availability", "online")
        self._mqtt.publish_message(self._device_name + "/state", "disarmed")

        self.login()

        self._logger.logInfo('MQTT: Creating alarm panel device')
        self.setupMQTTAlarmControlPanel()

        for alarm_status in self._alarm_statuses:
            self._logger.logInfo(f'MQTT: Creating binary sensor for alarm status "{alarm_status}"')
            self.setupMQTTAlarmSensors(alarm_status)

        self.createSensors()

    def on_disconnect(self, client, userdata, rc):
        """MQTT disconnect callback"""
        if rc != 0:
            self._logger.logWarning('Unexpected disconnection from MQTT, trying to reconnect')
            # recon()

    def on_message(self, client, userdata, message):
        """MQTT message handler"""
        msg_data = str(message.payload.decode("utf-8"))
        self._logger.logInfo(f'MQTT message received on "{message.topic}": {msg_data}')

        # Change the status: arm/disarm
        if message.topic == f'{self._device_name}/command':
            if msg_data == 'DISARM':
                result = self.disarm()
                if result == 1:
                    self._mode = CONST.MODE_DISARM
                    self._mqtt.publish_message(f'{self._device_name}/state', "disarmed")
            elif msg_data == 'ARM_AWAY':
                result = self.arm_away()
                if result == 1:
                    self._mode = CONST.MODE_ARM_AWAY
                    self._mqtt.publish_message(f'{self._device_name}/state', "armed_away")
            elif msg_data == 'ARM_HOME':
                result = self.arm_home1()
                if result == 1:
                    self._mode = CONST.MODE_ARM_HOME1
                    self._mqtt.publish_message(f'{self._device_name}/state', "armed_home")

        # Delegate incoming MQTT messages to each sensor
        for id in self._sensors:
            self._sensors[id].onMessage(client, userdata, message, msg_data)

    def login(self):
        """Login to the device."""
        self._connection.refreshToken()

    def get_version(self):
        """Get the software version of the device."""
        response = self._connection.get('firmwareGet')
        return response['updates']['xver']

    def disarm(self):
        """Disarm the device."""
        response = self._connection.post('panelCondPost', {"area": 1, "mode": 0})
        return response['result']

    def arm_away(self):
        """Arm the device (away mode)."""
        response = self._connection.post('panelCondPost', {"area": 1, "mode": 1})
        return response['result']

    def arm_home1(self):
        """Arm the device (Home 1 mode)."""
        response = self._connection.post('panelCondPost', {"area": 1, "mode": 2})
        return response['result']

    def getSensors(self):
        """Get the list of sensors."""
        response = self._connection.post('deviceGet', {"max_count": True})
        return response.get('senrows')

    def createSensors(self):
        """Create objects for each supported sensor."""
        sensors = self.getSensors()
        for data in sensors:
            sensor = self.newSensor(data)
            if sensor is not None:
                self._sensors[data.get('sid')] = sensor

    def sendPanelUpdates(self):
        """Send the current status (disarmed, armed_away, armed_home) to MQTT."""
        response = self._connection.get('panelCondGet')
        mode = int(response.get('forms').get('pcondform1').get('mode'))
        if mode != self._mode:
            ha_mode = CONST.MODES_MAP.get(mode)
            self._mode = mode
            self._mqtt.publish_message(f'{self._device_name}/state', ha_mode)

    def sendSensorUpdates(self):
        """Send the current sensor statuses to MQTT."""
        active_statuses = []
        for data in self.getSensors():
            sid = data.get('sid')
            sensor = self._sensors.get(sid)
            if sensor is not None:
                updated = sensor.updateFromData(data)
                if updated:
                    sensor.sendUpdate()
                # If this sensor has an alarm state, add it to the list of active states
                if sensor.alarmStatus:
                    self._logger.logInfo(f'Sensor {sensor} has alarm status {sensor.alarmStatus}')
                    if sensor.alarmStatus not in active_statuses:
                        active_statuses.append(sensor.alarmStatus)

        # If any sensor has an alarm state, update the state on MQTT
        for alarm_status in self._alarm_statuses:
            alarm_status_lower = alarm_status.lower()
            if alarm_status in active_statuses and self._alarm_statuses[alarm_status] != 'ON':
                self._alarm_statuses[alarm_status] = 'ON'
                self._mqtt.publish_message(f'{self._device_name}/{alarm_status_lower}_state', 'ON')
            elif alarm_status not in active_statuses and self._alarm_statuses[alarm_status] != 'OFF':
                self._alarm_statuses[alarm_status] = 'OFF'
                self._mqtt.publish_message(f'{self._device_name}/{alarm_status_lower}_state', 'OFF')

    def newSensor(self, data):
        """Create a new sensor object."""
        area = data.get('area')
        zone = data.get('zone')
        name = data.get('name')
        type = data.get('type')

        # Currently, only zone 1 is supported
        if area != 1:
            self._logger.logInfo(f'Skipping {name}, type {type}, area {area}, zone {zone}')
            return None

        if type == CONST.TYPE_DOOR_WINDOW:
            return DoorWindowSensor(data, self)
        elif type == CONST.TYPE_POWER_SWITCH_INTERNAL:  # TODO: Add IDs for other switch types
            return PowerSwitch(data, self)
        elif type in CONST.TYPE_ALARM:
            return AlarmSensor(data, self)
        else:
            self._logger.logInfo(f'Skipping "{name}", type {type}, area {area}')
        return None

    @property
    def manufacturer(self):
        return self._manufacturer

    @property
    def device_name(self):
        return self._device_name

import configparser
import os
import time
from lupus_to_mqtt.Panel import Panel
from lupus_to_mqtt.Logger import Logger
from lupus_to_mqtt.MQTT import MQTT

# Read configuration file
config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.abspath(__file__)) + '/config/config.ini')

MQTTServer = config['MQTT']['MQTTServer']
MQTTPort = int(config['MQTT']['MQTTPort'])
MQTTKeepalive = int(config['MQTT']['MQTTKeepalive'])
MQTTUser = config['MQTT']['MQTTUser']
MQTTPassword = config['MQTT']['MQTTPassword']
DeviceName = config['MQTT']['DeviceName']

LupusHost = config['Lupus']['LupusHost']
LupusUsername = config['Lupus']['LupusUsername']
LupusPassword = config['Lupus']['LupusPassword']
Manufacturer = config['Lupus']['Manufacturer']
Model = config['Lupus']['Model']

logger = Logger.getInstance()


def on_connect(client, userdata, flags, rc):
    panel.on_connect(client, userdata, flags, rc)


def on_disconnect(client, userdata, rc):
    panel.on_disconnect(client, userdata, rc)


def on_message(client, userdata, message):
    panel.on_message(client, userdata, message)


if __name__ == '__main__':
    mqtt = MQTT(MQTTServer, MQTTPort, MQTTKeepalive, MQTTUser, MQTTPassword)

    panel = Panel(DeviceName, LupusHost, LupusUsername, LupusPassword, Manufacturer, Model)

    # Define the mqtt callbacks
    mqtt.client.on_connect = on_connect
    mqtt.client.on_message = on_message
    mqtt.client.on_disconnect = on_disconnect
    mqtt.client.will_set(DeviceName + "/availability", payload="offline", qos=0, retain=True)

    # Connect to the MQTT server
    while True:
        try:
            mqtt.connect()
            break
        except:
            logger.warning_msg('Can\'t connect to MQTT broker. Retrying in 10 seconds.')
            time.sleep(10)

    mqtt.client.loop_start()
    while True:
        try:
            time.sleep(5)
            panel.sendPanelUpdates()
            panel.sendSensorUpdates()
            pass
        except KeyboardInterrupt:
            mqtt.client.loop_stop()
            break

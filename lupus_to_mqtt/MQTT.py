import sys
import time

import paho.mqtt.client as mqtt

from lupus_to_mqtt.Logger import Logger


class MQTT():
    """Manage the connection to an MQTT broker."""
    _instance = None

    @staticmethod
    def getInstance():
        """ Static access method (singleton pattern)."""
        return MQTT._instance

    def __init__(self, server, port, keepalive, user, password):
        """ Virtually private constructor (singleton pattern)."""
        if MQTT._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            MQTT._instance = self

        self._server = server
        self._port = port
        self._keepalive = keepalive
        self._user = user
        self._password = password

        self.logger = Logger.getInstance()

        self.client = mqtt.Client('lupus-to-mqtt')
        if user is not False and password is not False:
            self.client.username_pw_set(user, password)

    def connect(self):
        """Connect to the MQTT broker."""
        self.client.connect(self._server, self._port, self._keepalive)

    def publish_message(self, path, message):
        """Publish the given message on the MQTT broker."""
        try:
            self.client.publish(path, payload=message, qos=0, retain=True)
        except:
            self.logger.logWarning(f'Publishing "{message}" to {path} failed. Exception: {sys.exc_info()}')
        else:
            self.logger.logDebug(f'Published "{message}" to {path}')

    def delete_message(self, path):
        """Delete a given path from the broker."""
        try:
            self.client.publish(path, payload="", qos=0, retain=False)
        except:
            self.logger.logWarning(f'Deleting {path} failed. Exception: {sys.exc_info()}')
        else:
            time.sleep(0.1)
            self.logger.logDebug(f'Deleted {path}')

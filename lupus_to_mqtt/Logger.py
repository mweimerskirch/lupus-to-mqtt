import time

from lupus_to_mqtt.Formatting import Formatting


class Logger:
    """Output formatted log messages."""
    debug = True  # FIXME: Make configurable
    _instance = None

    @staticmethod
    def getInstance():
        """Static access method (singleton pattern)."""
        if Logger._instance is None:
            Logger()
        return Logger._instance

    def __init__(self):
        """Virtually private constructor (singleton pattern)."""
        if Logger._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Logger._instance = self

    def getTimestamp(self):
        """Get timestamp for the log message."""
        return time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())

    def logDebug(self, message):
        """Output an "debug" type log message."""
        if self.debug is True:
            print(f'{Formatting.SUCCESS}{self.getTimestamp()} | DEBUG: {message}{Formatting.END}')

    def logWarning(self, message):
        """Output an "warning" type log message."""
        print(f'{Formatting.WARNING}{self.getTimestamp()} | WARNING: {message}{Formatting.END}')

    def logInfo(self, message):
        """Output an "info" type log message."""
        print(f'{Formatting.INFO}{self.getTimestamp()} | INFO: {message}{Formatting.END}')

import demjson
from lupus_to_mqtt.Logger import Logger
import requests
import urllib3


class Connection:
    """Manage the connection to the alarm API."""
    _instance = None

    @staticmethod
    def getInstance():
        """Static access method (singleton pattern)."""
        return Connection._instance

    def __init__(self, host, username, password, verify_ssl):
        """Virtually private constructor (singleton pattern)."""
        if Connection._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Connection._instance = self
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.api_url = "{}/action/".format(host)
        self.headers = None
        self.verify = verify_ssl

        # Disable SSL warnings if "VerifySSL" is set to false in the configuration
        if not self.verify:
            urllib3.disable_warnings()

        self._logger = Logger.getInstance()

    def refreshToken(self):
        """Refresh the API token."""
        response = self.get('tokenGet')

        if response['result'] == 1:
            self._logger.logInfo('Token refreshed.')
            token = response['message']
            self.headers = {"X-Token": token}
        else:
            self._logger.logWarning('Could not get new token.')
        #     TODO: Handle error

    def _request_get(self, action):
        """Build the HTTP request for a GET action."""
        response = self.session.get(self.api_url + action, timeout=15, headers=self.headers, verify=self.verify)
        self._logger.logDebug(f'Sent GET to {action}. Response: {response.status_code}')
        return response

    def _request_post(self, action, params=None):
        """Build the HTTP request for a POST action."""
        if params is None:
            params = {}
        response = self.session.post(self.api_url + action, timeout=15, data=params, headers=self.headers, verify=self.verify)
        self._logger.logDebug(f'Sent POST to {action}. Response: {response.status_code}')
        return response

    def decode_response(self, text: str):
        """Decode a response from the server."""
        text = demjson.decode(text)
        return text

    def get(self, action):
        """Send a GET request the API and return the response."""
        response = self._request_get(action)
        response = self.decode_response(response.text)
        return response

    def post(self, action, params):
        """Send a POST request the API and return the response."""
        response = self._request_post(action, params)
        response = self.decode_response(response.text)
        return response

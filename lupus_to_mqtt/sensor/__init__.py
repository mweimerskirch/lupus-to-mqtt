import abc

class Sensor(metaclass=abc.ABCMeta):
    def __init__(self, data, panel):
        self._area = data.get('area')
        self._zone = data.get('zone')
        self._name = data.get('name')
        self._type = data.get('type')

        self._cond = data.get('cond')
        self._cond_ok = data.get('cond_ok')

        self._battery = data.get('battery')
        self._battery_ok = data.get('battery_ok')

        self._tamper = data.get('tamper')
        self._tamper_ok = data.get('tamper_ok')
        self._bypass_tamper = data.get('bypass_tamper')

        self._bypass = data.get('bypass')

        self._sid = data.get('sid')
        self._id = self._sid.replace(':', '_')
        self._su = data.get('su')
        self._alarm_status = data.get('alarm_status')
        self._status_ex = data.get('status_ex')

        self._panel = panel

    # def update(self, json_state):
    #     if self._type in CONST.TYPE_BINARY_SENSOR:
    #         self._json_state['status'] = json_state['status']
    #     else:
    #         self._json_state.update(
    #             {k: json_state[k] for k in json_state if self._json_state.get(k)})

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def sid(self):
        return self._sid

    @property
    def alarmStatus(self):
        return self._alarm_status

    def isBurglarAlarm(self):
        return self._alarm_status == 'BURGLAR'

    @abc.abstractmethod
    def updateFromData(self, data):
        pass

    @abc.abstractmethod
    def sendUpdate(self):
        pass
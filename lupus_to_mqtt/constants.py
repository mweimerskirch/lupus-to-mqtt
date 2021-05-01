# Sensor types
TYPE_REMOTE = 2
TYPE_DOOR_WINDOW = 4
TYPE_WATER = 5
TYPE_MOTION_SENSOR = 9
TYPE_SMOKE_DETECTOR = 11
TYPE_POWER_SWITCH_INTERNAL = 24
TYPE_KEYPAD = 37
TYPE_SIREN = 46

# Alarm modes
MODE_DISARM = 0
MODE_ARM_AWAY = 1
MODE_ARM_HOME1 = 2
MODE_ARM_HOME2 = 3

# Alarm modes mapped to HomeAssistant terms
MODES_MAP = {
    MODE_DISARM: 'disarmed',
    MODE_ARM_AWAY: 'armed_away',
    MODE_ARM_HOME1: 'armed_home',
    MODE_ARM_HOME2: 'armed_night',
}

# List of supported alarm statuses
SUPPORTED_ALARM_STATUSES = [
    'BURGLAR',
    'DOORBELL',
    'SMOKE',
    'MEDICAL',
    'WATER',
    'PANIC',
    'EMERGENCY',
    'FIRE',
    'CO',
    'EMERGENCY',
    'GAS',
    'HEAT'
]

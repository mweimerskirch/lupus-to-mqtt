# Sensor types
TYPE_REMOTE = 2
TYPE_DOOR_WINDOW = 4
TYPE_WATER = 5
TYPE_MOTION_SENSOR = 9
TYPE_SHUTTER = 76
TYPE_SMOKE_DETECTOR = 11
TYPE_POWER_SWITCH_INTERNAL = 24
TYPE_KEYPAD = 37
TYPE_SIREN = 46
TYPE_ALARM = [
    TYPE_DOOR_WINDOW,
    TYPE_SIREN,
    TYPE_WATER,
    TYPE_KEYPAD,
    TYPE_SMOKE_DETECTOR,
    TYPE_MOTION_SENSOR
]

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

# Sensor response modes
RESPONSE_NONE = 0
RESPONSE_DELAY_1 = 1  # "Eingangsverzögerung 1"
RESPONSE_DELAY_2 = 2  # "Eingangsverzögerung 2"
RESPONSE_DOORBELL = 3
RESPONSE_ALARM_FOLLOW = 4
RESPONSE_ALARM_INSTANT = 5
RESPONSE_SMOKE = 6
RESPONSE_MEDICAL = 7
RESPONSE_WATER = 8
RESPONSE_PANIC_SILENT = 9
RESPONSE_PANIC = 10
RESPONSE_EMERGENCY = 11
RESPONSE_FIRE = 12
RESPONSE_CO = 13
RESPONSE_ALARM_OUTDOOR = 14
RESPONSE_EMERGENCY_SILENT = 15
RESPONSE_GAS = 18
RESPONSE_HEAT = 19
RESPONSE_LOG = 97  # "Logbucheintrag"
RESPONSE_LOG_IMAGES = 94  # "Logbucheintrag (Bilder)"
RESPONSE_ALARM_SILENT = 99

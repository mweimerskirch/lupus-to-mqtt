# Lupus-to-MQTT

Home Assistant integration for Lupus Security (also known as "Lupusec") alarm devices through MQTT.
Currently only tested with the **Lupusec XT3** model.

Not affiliated with "Lupus Security".

## What works

* Arming/disarming the alarm.
* Door/window sensors status (open/closed).
* Turning the internal switch on/off.

## Current limitations

* Only one area is supported (the Lupusec XT3 can theoretically manage two areas).
* Only one "Home" mode is supported (the Lupusec XT3 can theoretically manage up to three home modes).
* Sensors without names are ignored.

## Manual installation

Copy config/config.ini.dist to config/config.ini and adjust the settings to your environment.

* The "DeviceName" is used for the MQTT paths as well as for the entity names in Home Assistant, so only use alphanumerical characters or underscore.
* The "Manufacturer" and "Model" are used for the labels in the HomeAssistant entity list.

Next, you need to install the requirements:

```shell
pip3 install -r requirements.txt
```

The application can then be run using:

```shell
python3 main.py
```
## Installation using Docker

Prepare the config file as described above.

You can build your docker image:
```shell
docker build -t lupusec2mqtt .
```

and then run it using docker-compose:

```shell
docker-compose up
```

## Configuring HomeAssistant Lovelace

You can add the following card to your Lovelace UI:

```yaml
type: alarm-panel
states:
  - arm_away
  - arm_home
entity: alarm_control_panel.lupus_to_mqtt
name: Alarmzentral
``` 

The suffix "lupus_to_mqtt" corresponds to whatever you set as the device id in your config file.

# Lupus-to-MQTT

Home Assistant integration for Lupus Security (also known as "Lupusec") alarm devices through MQTT.
Currently only tested with the **Lupusec XT3** model.

Not affiliated with "Lupus Security".

## What works

* Arming/disarming the alarm.
* Door/window sensors status (open/closed).

## Current limitations

* Only one area is supported (the Lupusec XT3 can theoretically manage two areas).
* Only one "Home" mode is supported (the Lupusec XT3 can theoretically manage up to three home modes).

## Configuring HomeAssistant Lovelace

You can add the following card to your Lovelace UI:

```yaml
type: alarm-panel
states:
  - arm_away
  - arm_home
entity: alarm_control_panel.lupus_xt3
name: Alarmzentral
``` 

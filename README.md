# es410_autonomous_drone
Warwick Engineering ES410 Group Project - Group 13

Repository to contain all of the code across 3 devices:

Raspberry Pi
- main.py
- landing_vision.py
- ground_communication.py
- flight_controller.py
- micro_controller.py
- data_logger.py
    
Arduino
- main.ino
    
Ground Control Station
- base_station.py

## User Guide

### Drone
_mostly written for the benefit of whoever writes the GCS code_

When drone is in **idle** state,
| Command | Description |
|---------|-------------|
|`shutdown`| shutdown drone |
|`mission`^ | send mission|

^ mission command should be of the following form ????

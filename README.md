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

# User Guide

## Drone
_mostly written for the benefit of whoever writes the GCS code_

#### State: Initialisation
Drone tries to establish connections to other parts of the system. A variety of messages sent. If successful, final message reported is `Initialisation successful.`. If initialisation fails, failure reported then the python program exits. Decided not to reboot else might get stuck in an endless cycle where we can't do anything with the pi.

#### State: Idle
| Command | Description | Expected response |
|---------|-------------|-------------------|
|`shutdown`| shutdown (power off) drone | `Drone is shutting down.` |
|`reboot`| reboot drone | `Drone is rebooting.`
|`mission`† | send mission |

† After mission command, mission details must be received within 5 seconds. Details should be of the following form ????

#### State: Wait for battery load
Battery must be connected in 20 seconds. GCS must confirm battery has been secured in a further 20 s with command `battery secured`.

#### State: Wait for parcel load
Parcel must be loaded within 30 seconds.

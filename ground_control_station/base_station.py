# ES410 Autonomous Drone
# Owner: James Bennett
# File: base_station.py
# Description: File to run locally on a laptop acting as the ground control station.

from drone_communication import DroneComms
import sys
import os
import json
import time

test = "mission"  # mission, logging


def wait_for_message(message, failed="None"):
    """
    prints messages from drone until specified message is received
    does not print specified message
    """
    while True:
        rec = drone.read_message()
        if rec != message and rec != failed and rec is not None:
            print("   Message from drone: " + rec)
        elif rec == message:
            # Return without printing anything
            return True
        elif rec == failed:
            return False


def verify(action):
    """
    Simply prompt the user to confirm they are sure
    """
    print("Are you sure you want to " + action + "?")
    return get_response("Response (y/n): ")


def get_response(prompt):
    """
    Get a yes or no response from the command line
    """
    ans = input(prompt)
    while ans not in ('y', 'n'):
        print("Response not recognised. Try again.")
        ans = input(prompt)
    return ans


def clear():
    """
    Clear command line issue command based on os
    """
    if sys.platform == 'win32':
        os.system('cls')
    elif sys.platform == 'linux':
        os.system('clear')


def abort_setup():
    """
    Abort the setup and clear the command line
    """
    print("\n Aborting setup. Please wait for drone to timeout and be ready to receive a command. \n")
    time.sleep(3)
    clear()


if test == "mission":
    while True:
        # === DRONE STATE: INITIALISING ===
        # trying to connect to drone
        print("Trying to connect to drone...")
        try:
            drone = DroneComms()
        except Exception as e:
            print(e)
            print("Failed to connect to drone. Would you like to try again?")
            response = input("Response (y/n): ")
            if response == 'y':
                continue
            elif response == 'n':
                break
        else:
            print("Connection established. Waiting for drone to initialise...")

        # waiting for initialisation to be complete
        wait_for_message("Initialisation successful.")
        print("Drone Initialisation Complete.\n")
        break

    while True:
        # === DRONE STATE: IDLE ===
        print("Waiting for drone to confirm it is ready for a command...")
        wait_for_message("Drone is idle. Waiting for command.")  # this line mainly if user responds no
        print("Drone idle. Waiting for command.")
        command = input("Enter command: ")
        # --- shutdown ---
        if command == "shutdown":
            answer = verify("shutdown")
            if answer == 'y':
                drone.send_message("shutdown")
                wait_for_message("Drone is shutting down.")
                print("Drone shutting down.")
                while drone.is_comms_open():
                    # use this to verify drone is shutting down.
                    continue
                print("Connection to drone lost. Exiting program.")
                sys.exit()
            elif answer == 'n':
                abort_setup()
                continue  # go back to idle state
            else:  # problem
                print("Problem. This shouldn't have happend. Quitting.")
                sys.exit()

        # --- reboot ---
        elif command == "reboot":
            answer = verify("reboot")
            if answer == 'y':
                drone.send_message("reboot")
                wait_for_message("Drone is rebooting.")
                print("Drone rebooting.")
                while drone.is_comms_open():
                    # use this to verify drone is shutting down.
                    continue
                print("Connection to drone lost. Exiting program.")
                sys.exit()
            elif answer == 'n':
                abort_setup()
                continue  # go back to idle state
            else:  # problem
                print("Problem. This shouldn't have happend. Quitting.")
                sys.exit()

        # --- mission ---
        elif command == "mission":
            print("Please enter the mission details.")
            # store values in a dictionary then send encoded as json
            mission = {"title": input("  Mission Title: "),
                       "location": input("  Mission destination: "),
                       "altitude": int(input("  Mission altitude: "))}

            # encode mission as json
            str_mission = json.dumps(mission)
            # send "mission" to put drone in state ready to receive mission details
            drone.send_message("mission")
            # send mission details
            drone.send_message(str_mission)

            print("Mission sent. Drone is processing the mission. Please wait.")
            wait_for_message("Mission processing finished.")
            print("Mission upload complete. \n")

        # === DRONE STATE: BATTERY LOADING ===
        print("Please load battery into the drone.")
        wait_for_message("Battery connected.")
        print("Battery is connected. Please confirm the battery is secured.")
        response = get_response("Is battery secured (y/n): ")
        if response == 'y':
            drone.send_message("battery secured")
            wait_for_message("Battery loaded.")
            print("Battery load complete.\n")
        elif response == 'n':
            abort_setup()
            continue  # go back to idle state
        else:  # problem
            print("Problem. This shouldn't have happend. Quitting.")
            sys.exit()

        # === DRONE STATE: PARCEL LOADING ===
        print("Please hold parcel underneath drone and press button to close the grippers.")
        if wait_for_message("Parcel loaded.", "Failed to load parcel."):
            print("Parcel successfully loaded.\n")
        else:
            print("Failed to load parcel.\n")
            continue

        # === DRONE STATE: CHECK DRONE IS ARMABLE ===
        print("Checking drone is armable.")
        if wait_for_message("Drone ready to arm.", "Arming check failed."):
            print("Drone is ready to arm.\n")
        else:
            print("Arming check failed.\n")
            continue

        """ CURRENTLY NOT BEING USED
        # === DRONE STATE: WAITING FOR HWSS ===
        print("Please press the hardware safety switch.")
        wait_for_message("Switch pressed.")
        print("Switch pressed. Pausing to allow all people to withdraw to a safe distance. \n")
        """

        # === DRONE STATE: WAITING FOR FLIGHT AUTHORISATION ===
        wait_for_message("Waiting for authorisation to fly.")
        print("Drone is ready to fly. Awaiting authorisation to begin flight.")
        print(" **WARNING: when you grant authorisation the drone will take off. Ensure it is safe to begin flight.** ")
        print("Enter \"takeoff\" to begin the flight or \"cancel\" to abort")

        command = input("Command: ")
        while command not in ('takeoff', 'cancel'):
            print("Response not recognised, please enter \"takeoff\" or \"cancel\"")
            command = input("Command: ")

        if command == "takeoff":
            drone.send_message("takeoff")
            wait_for_message("Authorisation received.")
            print("Authorisation received by drone. Beginning flight imminently")
        # continue with program
        elif command == "cancel":
            abort_setup()
            continue  # go back to idle state
        else:  # problem
            print("Problem. This shouldn't have happend. Quitting.")
            sys.exit()

        # === DRONE STATE: FLYING ===
        print("Drone is in flight mode. Messages from drone will be reported.")
        msg = None
        while msg != "Flight complete. Drone at home.":
            if msg is not None:
                print("  " + msg)
            msg = drone.read_message()
        print("Flight complete. Drone at home.")
        clear()
    # drone will go back to idle state

    # after while loop, exit program
    quit()

if test == "logging":
    while True:
        # === DRONE STATE: INITIALISING ===
        # trying to connect to drone
        print("Trying to connect to drone...")
        drone = DroneComms()
        try:
            pass
        except:

            print("Failed to connect to drone. Would you like to try again?")
            response = input("Response (y/n): ")
            if response == 'y':
                continue
            elif response == 'n':
                break
        else:
            print("Connection established. Waiting for drone to initialise...")

        # waiting for initialisation to be complete
        wait_for_message("Initialisation successful.")
        print("Drone Initialisation Complete.\n")
        break

    while True:
        # === DRONE STATE: IDLE ===
        received = drone.read_message()
        if received is not None:
            print(received)

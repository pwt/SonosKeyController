# SonosKeyController script. Converts key-presses into
# SoCo commands.

import datetime
import os
import sys
import signal
import soco

from soco_cli import api

# Pull in the configuration from your config.py
from config import commands
from config import speaker_ip
from config import room_name


# Wait for a keypress and return
def wait_for_keypress():
    result = None
    if os.name == "nt":  # Windows (UNTESTED)
        import msvcrt

        result = msvcrt.getch()
    else:  # Unix
        import termios

        fd = sys.stdin.fileno()
        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    return result


# SIGINT (CTRL-C) Handler
def sigint_handler(signum, frame):
    print("CTRL-C ... exiting.")
    exit(0)


def play_favourite(speaker, favourite):
    exit_code, output, error_msg = api.run_command(
        speaker.ip_address, "play_fav", favourite
    )
    return False if exit_code else True


def queue(speaker):
    exit_code, output, error_msg = api.run_command(speaker.ip_address, "queue")
    print(output, "\n")
    while True:
        try:
            queue_number = int(input("Enter queue number to play, or 0 to cancel: "))
            break
        except ValueError:
            print("Error: integer required")
    if queue_number < 1:
        return
    try:
        speaker.play_from_queue(queue_number - 1, start=True)
    except Exception as error:
        print("Error: {}".format(error))


def favourites(speaker):
    exit_code, output, error_msg = api.run_command(speaker.ip_address, "lf")
    print(output, "\n")
    while True:
        fav_number = input("Enter favourite number to play, or 0 to cancel: ")
        if fav_number == "0":
            break
        exit_code, output, error_msg = api.run_command(
            speaker.ip_address, "pfn", fav_number
        )
        if exit_code == 0:
            break
        else:
            print(error_msg)


if __name__ == "__main__":

    # Catch CTL-C
    signal.signal(signal.SIGINT, sigint_handler)

    # Create the SoCo speaker object
    if speaker_ip:
        speaker = soco.SoCo(speaker_ip)
    else:
        speaker = soco.discovery.by_name(room_name)

    if not speaker:
        print("Speaker not found ... exiting")
        exit(0)
    else:
        print("Sending commands to speaker '{}'".format(speaker.player_name))

    print("Waiting for input ... use CTL-C to quit")

    # Input loop
    while True:
        code = wait_for_keypress()
        timestamp = str(datetime.datetime.now())[:-7]
        if code in commands:
            try:
                command = commands[code]
                action = command[1]
                if action == "play":
                    speaker.play()
                    msg = command[0]
                elif action in ["pause", "stop", "off"]:
                    speaker.pause()
                    msg = command[0]
                elif action == "next":
                    speaker.next()
                    msg = command[0]
                elif action == "previous":
                    speaker.previous()
                    msg = command[0]
                elif action == "queue":
                    queue(speaker)
                    msg = command[0]
                elif action == "favs":
                    favourites(speaker)
                    msg = command[0]
                elif action == "relative_volume":
                    vol_change = int(command[2])
                    speaker.set_relative_volume(vol_change)
                    msg = command[0] + " " + str(vol_change)
                elif action == "favourite":
                    fav = command[2]
                    if play_favourite(speaker, fav):
                        msg = command[0] + ": " + fav
                    else:
                        msg = command[0] + ": Could not play " + fav
                print("{}: {}".format(timestamp, msg))
            except Exception as error:
                # Catch any other exceptions to keep running
                print("{}: Exception caught: {}".format(timestamp, error))
                pass
        else:
            print(
                timestamp + " : key = " + code + ": Unmapped ASCII = " + str(ord(code))
            )

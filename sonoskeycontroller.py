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
    # Wait for a key press on the console and return it
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
    fs = speaker.music_library.get_sonos_favorites(complete_result=True)
    the_fav = None
    # Strict match
    for f in fs:
        if favourite == f.title:
            the_fav = f
            break
    # Fuzzy match
    if not the_fav:
        favourite = favourite.lower()
        for f in fs:
            if favourite in f.title.lower():
                the_fav = f
                break
    if the_fav:
        # play_uri works for most favourites
        try:
            uri = the_fav.get_uri()
            metadata = the_fav.resource_meta_data
            speaker.play_uri(uri=uri, meta=metadata)
            return True
        except Exception as error:
            print("Error: {}".format(error))
            return False
    else:
        return False


def queue(speaker):
    exit_code, output, error_msg = api.run_command(speaker.ip_address, "queue")
    print(output)
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
    print(output)
    while True:
        try:
            fav_number = int(input("Enter queue number to play, or 0 to cancel: "))
            break
        except ValueError:
            print("Error: integer required")
    if fav_number < 1:
        return
    favs = speaker.music_library.get_sonos_favorites(complete_result=True)
    try:
        fav = favs[fav_number - 1]
        uri = fav.get_uri()
        metadata = fav.resource_meta_data
        speaker.play_uri(uri=uri, meta=metadata)
    except Exception as error:
        print("Error: {}".format(error))


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

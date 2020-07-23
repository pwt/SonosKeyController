# SonosKeyController script. Converts key-presses into
# requests to the SONOS HTTP API.

import datetime
import os
import sys
import signal

# Pull in the configuration from your config.py
from config import commands


# Wait for a keypress and return
def wait_for_keypress():
    # Wait for a key press on the console and return it.
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


# Catch CTL-C
signal.signal(signal.SIGINT, sigint_handler)

# Print config
print("")
for code in commands:
    # print(code + ' ' + commands[code][0] + " : " + commands[code][1])
    print(
        "Keycode: {} = {}".format(
            code,
            "sonos {} '{}' {}".format(
                commands[code][1], commands[code][2], commands[code][3]
            ),
        )
    )
print("\nWaiting for input ... use CTL-C to quit")

# Input loop
while True:
    code = wait_for_keypress()
    timestamp = str(datetime.datetime.now())[:-7]
    if code in commands:
        try:
            command = "sonos {} '{}' {}".format(
                commands[code][1], commands[code][2], commands[code][3]
            )
            print("{}: Command: {}".format(timestamp, command))
            os.system(command)
        except Exception as error:
            # Catch any other exceptions to keep running
            print("{}: Exception caught: {}".format(timestamp, error))
            pass
    else:
        print(timestamp + " : key = " + code + ": Unmapped ASCII = " + str(ord(code)))

# End of Script

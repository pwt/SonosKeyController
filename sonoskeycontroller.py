# SonosKeyController script. Converts keypresses into
# requests to the SONOS HTTP API.

import sys, os, requests, datetime

# Configuration Section #############################################

# Set up Room Name(s)
study = 'study'
front_reception = 'front%20reception'

# Set up the SONOS HTTP API Host. Can be 'localhost'.
hostname = '192.168.0.36'

# Assemble the root URL to use for SONOS HTTP API Requests
root_url = 'http://' + hostname + ':5005/' + front_reception + '/'

# Set up SONOS Favourites (if required). These must be identical to
# the favourite names set within SONOS. 

# 0 : Radio Paradise
# 1 : Jazz24
# 2 : BBC Radio 2
# 3 : BBC Radio 3
# 4 : BBC Radio 4
# 5 : Classic FM
# 6 : BBC Radio 6 Music 

zero = 'favorite/Radio%20Paradise%20UK%20AAC%20320kbps'
one = 'favorite/Jazz24%20-%20KNKX-HD2'
two = 'favorite/BBC%20Radio%202'
three = 'favorite/BBC%20Radio%203'
four = 'favorite/BBC%20Radio%204'
five = 'favorite/Classic%20FM'
six = 'favorite/BBC%20Radio%206%20Music'

# Command Matrix. Maps IR 'keypresses' to HTTP command URLs.

commands = {'r': ('PLAY', root_url + 'play'),
            'f': ('PAUSE', root_url + 'pause'),
            'x': ('STOP', root_url + 'pause'),
            '\'': ('OFF', root_url + 'pause'),
            '.': ('NEXT', root_url + 'next'),
            '1': ('ONE', root_url + one),
            '2': ('TWO', root_url + two),
            '3': ('THREE', root_url + three),
            '4': ('FOUR', root_url + four),
            '5': ('FIVE', root_url + five),
            '6': ('SIX', root_url + six),
            '7': ('SEVEN', root_url + ''),
            '8': ('EIGHT', root_url + ''),
            '9': ('NINE', root_url + ''),
            '0': ('ZERO', root_url + zero),
            '=': ('VOLUME_UP', root_url + 'volume/+10'),
            '-': ('VOLUME_DOWN', root_url + 'volume/-10'),
            ',': ('PREVIOUS', root_url + 'previous')}


# End Configuration Section #########################################

# Wait for a keypress and return
def wait_for_keypress():
    # Wait for a key press on the console and return it.
    result = None
    if os.name == 'nt':  # Windows
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


# Main Loop
print('Waiting for input ...')
while True:
    code = wait_for_keypress()
    timestamp = str(datetime.datetime.now())[:-7]
    if code in commands:
        try:
            r = requests.get(commands[code][1])
            if r.status_code == 200:
                print(timestamp + ' Success ' + commands[code][0] + ': ' + commands[code][1])
            else:
                print(timestamp + ' Sonos HTTP API request unsuccessful: HTTP Status = ' + \
                      str(r.status_code) + ' ' + commands[code][0] + ': ' + commands[code][1])
        except:  # PEP8 will flag this as a 'bare except'
            # Catch any other exceptions to keep running
            print (timestamp + ' Sonos HTTP API request unsuccessful')
            pass
    else:
        print(timestamp + ' : key = ' + code + ": Unmapped ASCII = " + str(ord(code)))

# End of Script

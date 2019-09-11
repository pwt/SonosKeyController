# Configuration Section #############################################

# 1. Set up the Room Name(s)
#    These must exactly match the room name(s) in your Sonos system.
#    Use '%20' for spaces; similarly encode other 'unsafe' URL characters

room = 'front%20reception'

# 2. Set up the hostname or IP address of the system running the Sonos HTTP API, and the port
#    Can be 'localhost'

sonos_api_host = '192.168.0.36'
sonos_api_port = '5005'

# Assemble the root URL to use for SONOS HTTP API Requests
base_url = 'http://' + sonos_api_host + ':' + sonos_api_port + '/' + room

# 3. Define the Command Matrix.
#    This maps key-presses to HTTP command URLs. Follow the pattern below to map keyboard inputs (the key on the left)
#    to the URLs to called in response. Extend or reduce the number of command lines as required.
#    Encode unsafe URL characters
#    Inspect the SONOS HTTP API documentation for available commands

commands = {'r':  ('PLAY', base_url + '/play'),
            'f':  ('PAUSE', base_url + '/pause'),
            'x':  ('STOP', base_url + '/pause'),
            '\'': ('OFF', base_url + '/pause'),
            '.':  ('NEXT', base_url + '/next'),
            '0':  ('ZERO', base_url + '/favorite/Radio%20Paradise'),  # Plays favourite 'Radio Paradise'
            '1':  ('ONE', base_url + '/favorite/Jazz24%20-%20KNKX-HD2'),
            '2':  ('TWO', base_url + '/favorite/BBC%20Radio%202'),
            '3':  ('THREE', base_url + '/favorite/BBC%20Radio%203'),
            '4':  ('FOUR', base_url + '/favorite/BBC%20Radio%204'),
            '5':  ('FIVE', base_url + '/favorite/Classic%20FM'),
            '6':  ('SIX', base_url + '/favorite/BBC%20Radio%206%20Music'),
            '=':  ('VOLUME_UP', base_url + '/volume/+10'),
            '-':  ('VOLUME_DOWN', base_url + '/volume/-10'),
            ',':  ('PREVIOUS', base_url + '/previous')
            }

# End Configuration Section #########################################

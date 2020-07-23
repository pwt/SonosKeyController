# Configuration Section #############################################

# STEP 1. Specify the Room Name
#         This must exactly match the room name in your Sonos system.

room = "Front Reception"  # The target Sonos Room/Zone
options = "-l"  # Options to pass to the 'sonos' command

# STEP 2. Define the Command Mappings.
#         This maps key-presses to commands. Follow the pattern below to map your choice of
#         keyboard inputs (the dictionary key on the left) to the 'sonos' commands used.
#         Extend or reduce the number of command lines as required.
#         (Inspect the soco-cli documentation for available commands.)

commands = {
    "r": ("PLAY", options, room, "play"),
    "f": ("PAUSE", options, room, "pause"),
    "x": ("STOP", options, room, "pause"),
    "'": ("OFF", options, room, "pause"),
    ".": ("NEXT", options, room, "next"),
    "0": ("ZERO", options, room, "play_fav 'RP World/etc'"),
    "1": ("ONE", options, room, "play_fav 'Jazz24'"),
    "2": ("TWO", options, room, "play_fav 'BBC Radio 2'"),
    "3": ("THREE", options, room, "play_fav 'BBC Radio 3'"),
    "4": ("FOUR", options, room, "play_fav 'BBC Radio 4'"),
    "5": ("FIVE", options, room, "play_fav 'Classic FM'"),
    "6": ("SIX", options, room, "play_fav 'BBC Radio 6'"),
    "9": ("NINE", "-lr", room, "vol"),
    "=": ("VOLUME_UP", options, room, "rv 10"),
    "-": ("VOLUME_DOWN", options, room, "rv -10"),
    ",": ("PREVIOUS", options, room, "previous"),
}

# End Configuration Section #########################################

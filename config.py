# Configuration Section #############################################

# STEP 1. Specify the Room Name OR IP Address
#         Name must exactly match the room name in your Sonos system.

# Set the Room Name ...
room_name = None  # The target Sonos Room/Zone
# ... OR set the speaker IP Address
speaker_ip = "192.168.0.35"


# STEP 2. Define the Command Mappings.
#         This maps key-presses to commands. Follow the pattern below to map your choice of
#         keyboard inputs (the dictionary key on the left) to the SoCo actions taken.
#         Extend or reduce the number of command lines as required.

commands = {
    # Format:
    # "Keystroke": ("DESCRIPTIVE TITLE", "Action", "Arguments"),
    "r": ("PLAY", "play"),
    "f": ("PAUSE", "pause"),
    "x": ("STOP", "pause"),
    "q": ("PRINT QUEUE", "queue"),
    "v": ("FAVOURITES", "favs"),
    "'": ("OFF", "pause"),
    ",": ("PREVIOUS", "previous"),
    ".": ("NEXT", "next"),
    "=": ("VOLUME_UP", "relative_volume", 5),
    "-": ("VOLUME_DOWN", "relative_volume", -5),
    "0": ("FAVOURITE ZERO", "favourite", "RP World/etc"),
    "1": ("FAVOURITE ONE", "favourite", "Jazz24"),
    "2": ("FAVOURITE TWO", "favourite", "BBC Radio 2"),
    "3": ("FAVOURITE THREE", "favourite", "BBC Radio 3"),
    "4": ("FAVOURITE FOUR", "favourite", "BBC Radio 4"),
    "5": ("FAVOURITE FIVE", "favourite", "Classic FM"),
    "6": ("FAVOURITE SIX", "favourite", "BBC Radio 6"),
    "7": ("FAVOURITE SEVEN", "favourite", "Scala"),
    "8": ("FAVOURITE EIGHT", "favourite", "Times Radio"),
    "9": ("FAVOURITE NINE", "favourite", "World Service"),
}

# End Configuration Section #########################################

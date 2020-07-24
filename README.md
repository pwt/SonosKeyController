# SonosKeyController

*Note: Previous versions of this script used the Sonos HTTP API instead of soco-cli. The move to soco-cli makes the script self-contained.*

This is a small Python script that waits for keyboard input at the console. Keyboard inputs trigger invocations of **soco-cli** [1], which is a command line utility for controlling various Sonos functions.

The script is especially useful with a **FLIRC** [2], a USB dongle that is programmed to recognise infrared (IR) codes from arbitrary IR remotes, and then translate them into keyboard key-presses. Using the script with a FLIRC enables IR control of Sonos systems.

The script can also be used with anything else that presents as a keyboard connected directly to the computer on which the script is running. Note that since the script runs as a console program, it's only really suitable for running on headless hosts. I run it on a Raspberry Pi near the Sonos Port that it controls.

## Requirements

A working Python 3.5+ environment running on a suitable host, with the **soco-cli** package installed (use PyPi).

The script is intended to run as a console program in order to accept keyboard input from a directly attached keyboard, FLIRC, etc.

The script is tested on Linux but includes **untested** support for Windows.

## Usage

The file `config.py` needs to be edited for your needs. See the steps within the file. The script is run using `python sonoskeycontroller.py`.

## Automatic Startup (Linux)

In order to start the program automatically on reboot, it's useful to:

#1 Be able to log in a special user automatically at the console. Note: this should not be any of the normal users, but a user specifically created for Sonos control purposes.

#2 Have the console session detected, in order to start the program in the console case only.

### Logging in automatically

For `systemd` based systems: create the following file if it doesn't exist:

```
sudo touch /etc/systemd/system/getty@.service.d/customexec.conf
```

Then edit the file to add the following section (replace 'sonos_user' with your required user name):

```
[Service]
ExecStart=
ExecStart=-/sbin/agetty --noclear --autologin sonos_user %I $TERM
```

This will automatically login 'sonos_user' at the console on every reboot.

### Starting sonoskeycontroller for the console sesssion only

In `.bashrc` (or the equivalent for your shell if you're not using bash), add the following at the end.

```
case $(tty) in /dev/tty[0-9]*)
    echo "Console Detected"
    python sonoskeycontroller.py
esac
```

Adjust the `python` command to suit your installation.

## Support

Just raise a GitHub issue if you'd like help with anything. I'll respond as promptly as I can.

## Links
[1] https://github.com/avantrec/soco-cli \
[2] https://flirc.tv/more/flirc-usb

"""Docstring.

Attributes:
    ACCESS_TOKEN (str): Access token of twitter
    ACCESS_TOKEN_SECRET (str): Access token secret of twitter
    API_KEY (str): Api key
    API_SECRET (str): Api secret
    auth (TYPE): Description
    debug (int): Debug flag
    localtime (TYPE): Current time
    twitter (TYPE): Description
    twitter_username (str): Username in twitter
    welcome_msg (TYPE): Welcome message
"""
# To share mouse gestures and post on Twitter
import struct
import time

# If it is not already installed, please download & install the twitter package from
# https://pypi.python.org/pypi/twitter
from twitter import *

debug = 1

API_KEY = 'XXXX'
API_SECRET = 'XXXX'
ACCESS_TOKEN = 'XXXX'
ACCESS_TOKEN_SECRET = 'XXXX'
twitter_username = 'XXXX'

localtime = time.asctime(time.localtime(time.time()))
auth = OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, API_KEY, API_SECRET)
twitter = Twitter(auth=auth)
welcome_msg = "\nWelcome to SecureTea..!! Initializing System @ " + localtime
print(welcome_msg)
twitter.direct_messages.new(user=twitter_username, text=welcome_msg)


def get_mouse_event():
    """Docstring.

    Returns:
        TYPE: Description
    """
    with open("/dev/input/mice", "rb") as fh:
        buf = fh.read(3)
        button = ord(buf[0])
        # what is the purpose of these? they're
        # not used...
        bLeft = button & 0x1
        bMiddle = (button & 0x4) > 0
        bRight = (button & 0x2) > 0
        x, y = struct.unpack("bb", buf[1:])

    return x, y


def notification_to_twitter(msg):
    """Docstring."""
    try:
        twitter.direct_messages.new(user=twitter_username, text=msg)
    except Exception as e:
        print("Notification not sent, error is: " + str(e))


def main():
    """Docstring."""
    alert_count = 1
    posx = 0
    posy = 0
    while(1):
        x, y = get_mouse_event()
        posx = posx + x
        posy = posy + y

        # It should be up to date, when the mouse moves even slightly
        if (debug == 1):
            print(posx, posy)

        # Laptops accessed someone by moving the mouse / touchpad
        if (posx > 100 or posy > 100 or posx < -100 or posy < -100):
            localtime = time.asctime(time.localtime(time.time()))

            msg = 'Alert(' + str(alert_count) + \
                ') : Someone has access your laptop when ' + localtime

            # Shows the warning msg on the console
            if (debug == 1):
                print(msg)

            # Send a warning message via twitter account
            notification_to_twitter(msg)
            # Reset / Update counter for the next move
            posx = 0
            posy = 0
            alert_count = alert_count + 1

            # Wait 10 seconds, to avoid too many Warning messages
            if (debug == 1):
                print("The program will sleep for 10 seconds")

            time.sleep(10)

            # Ready to monitor the next move
            if (debug == 1):
                print("Ready to monitor further movement .. !!")


if __name__ == '__main__':

    main()
    print("End of program")

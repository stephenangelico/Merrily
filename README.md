# Merrily
IP doorbell alert system
Named for the line in Gilbert and Sullivan's Princess Ida "Merrily ring the luncheon bell".

When someone presses the doorbell, a notification should pop up on any connected clients.

This project arose out of a personal need to make the household doorbell more
noticeable when no occupants are able to hear a normal ring.
The reference design includes a Raspberry Pi connected via the GPIO pins to a
charge-discharge circuit (details in merrily/doorbell.py), connected to the
speaker leads on the doorbell. When a ring is detected, a HTTP POST request is
sent to the server which sends notifactions as appropriate.

Installation
============

Tested on Ubuntu MATE 16.04 and 17.04 but should work on any system with
Python 3.4+ and `notify-send`.


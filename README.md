# Merrily
IP doorbell alert system

Named for the song in Princess Ida "Merrily ring the luncheon bell".

When the doorbell is pressed, a notification should appear on connected clients.

This project arose out of a personal need to make the household doorbell more
noticeable when no occupants are able to hear a normal ring.
The reference design includes a Raspberry Pi 3 Model B connected via the GPIO
pins to a charge-discharge circuit (details in `doorbell.py`), which in
turn is connected to the speaker leads on the doorbell. When a ring is detected,
any connected clients will be sent a notification using `notify-send`.

Also included is an optional web-based logging system built with Flask and
PostgreSQL, however, this requires more setup than the main notifier.

Installation
============

Tested on Ubuntu MATE 16.04 and up, but should work on any system with
Python 3.4+ and `notify-send`. VLC is also used to play
the alert tone, but can be substituted with any media player.
Install those from your package manager if they are not installed already.

Clone or download:
```bash
git clone https://github.com/stephenangelico/Merrily.git
cd Merrily
```

If you are setting up the doorbell sensor, install dependencies:
```bash
python3 -m pip install -r requirements.txt
```

Copy `config_example.py` to `config.py` and modify it as necessary.

If you just want to run the client, see [Running](#running).

Connecting to your doorbell
===========================

The reference design for this project uses a charge-discharge circuit made with
2 100KΩ resistors and a 10nF capacitor. Information on creating this circuit can
be found [here](https://www.allaboutcircuits.com/projects/building-raspberry-pi-controllers-part-5-reading-analog-data-with-an-rpi/).
You don't need to follow it to the letter, but check a pinout diagram (such as
[this one](https://cdn.sparkfun.com/assets/learn_tutorials/4/2/4/header_pinout.jpg))
and connect the wires to two GPIO pins (green in the suggested diagram) and one
ground (black in the same diagram).

Take note of which **GPIO** pins you are connecting to. This is not the same
as the geographical pin number. For instance, geographical pin 12 represents
GPIO pin 18. Replace the values for `A_PIN` and `B_PIN` in `config.py` with
those you took note of.

Next you need to establish your threshold for what represents a ringing signal.
`doorbell.py` has some functions to help you figure out the level you need.
Run it with the `testring` argument (from the virtual environment):

```bash
python doorbell.py testring
120
120.9
120.65
120.975
```

This function does the same thing as the main looping function (but with print()
calls so you know what's going on) - calculate the average time to charge over
the last second. Look at this number when the doorbell is silent, then watch the
value as you press the doorbell.

Pick a boundary value to replace the value in the `if` statement in the function
and test it this way until it correctly rings for every ring and does not ring
at other times.

Depending on which way the speaker is attached to the circuit, a signal on the
line may cause the charge time to become high or low. Check that the operator
is correct for this situation. So if a ring causes the level to drop, a ring
event should trigger if the level becomes less than (<) a particular value.

Once you have settled on a value, set it as `THRESHOLD` in `config.py`, and the
hardware should be good to go.

Running
=======

Main doorbell daemon:

```bash
python3 doorbell.py
```

Server to broadcast notifications:

```bash
python3 blanche.py
```

Client to receive notifications:

```bash
python3 cyril.py
```

Make sure to specify the correct host to connect to in `config.py`. Also check
that the media player command is correct or empty brackets (ie `[]`).

There is also an installer to create and start SystemD services for each module:

```bash
python3 install.py --help
```


Protocol:
=========

Two-way socket connection between doorbell and listeners.
The publisher, or server, is the doorbell. The listening clients are any
machines wishing to be rung with the doorbell. The server will treat any
connection as a subscription to all events.

All messages between the server and clients MUST terminate with '\r\n'.
Upon connection, the server will greet with "Latest Ring: <id> <time> <source>"
When the doorbell rings, the server emits an event "New Ring: <id> <time> <source>".
Clients should compare the ring ID with the latest ID that they have heard, and
take action as desired.

If the server resets, it may emit a lower ring ID than a client had heard
previously. In this case, the client should check if the new timestamp is later
than the previously stored one.

Ring IDs will be monotonically increasing positive integers. An ID of 0 means no
last ring. Timestamps will sent as Unix time. Source will be "None" if ID is 0,
or an address (eg "127.0.0.1:12345").

Ring events are triggered by privileged clients authenticated by sending a
pre-shared token to the server thus: "Token: asdf1234"
Without token authentication, clients cannot broadcast ring events.
It is recommended that the doorbell sensor and server run on the same machine.

Clients may send heartbeats to the server with "Heartbeat: Send" which will
receive the response "Heartbeat: Response".

# Merrily
IP doorbell alert system

Named for the song in Princess Ida "Merrily ring the luncheon bell".

When the doorbell is pressed, a notification should appear on connected clients.

This project arose out of a personal need to make the household doorbell more
noticeable when no occupants are able to hear a normal ring.
The reference design includes a Raspberry Pi 3 Model B connected via the GPIO
pins to a charge-discharge circuit (details in `doorbell.py`), which in
turn is connected to the speaker leads on the doorbell. When a ring is detected,
any connected clients will be sent the string "Doorbell!". The included
`client.py` will listen for that string and send a desktop notification using
`notify-send`.

Also included is an optional web-based logging system built with Flask and
PostgreSQL, however, this requires more setup than the main notifier.

Installation
============

Tested on Ubuntu MATE 16.04 and up, but should work on any system with
Python 3.4+ (with venv and pip) and `notify-send`. VLC is also used to play
the alert tone, but can be substituted with any media player.
Install those from your package manager if they are not installed already.

Clone or download:
```bash
git clone https://github.com/stephenangelico/Merrily.git
cd Merrily
```

Create virtual environment (recommended):
```bash
python3 -m venv env
source env/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Copy `config_example.py` to `config.py` and modify it as necessary.

If you just want to run the client, scroll right down to [Running](#running).

Log server setup (optional)
===========================

The log server requires a configured PostgreSQL server. Run these commands from
the installation directory or virtual environment.

Create database:
```bash
createdb merrily
```

If for whatever reason you want to run the unit tests as well:
```bash
createdb merrily-test
```
Note that the tests require that the testing database be empty to begin with.
The tests can then be run from the environment with `python tests.py`.

Create a user for web interface:
```bash
python log_server.py adduser
```

Modify `config.py` with your database credentials.

Connecting to your doorbell
===========================

The reference design for this project uses a charge-discharge circuit made with
2 100KΩ resistors and a 10nF capacitor. Information on creating this circuit can
be found [here](https://www.allaboutcircuits.com/projects/building-raspberry-pi-controllers-part-5-reading-analog-data-with-an-rpi/).
You don't need to follow it to the letter, but check a pinout diagram (such as
[this one](https://goo.gl/images/bU7u56)) and connect the wires to two GPIO pins
(green in the suggested diagram) and one ground (black in the same diagram).
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

Run all commands in the virtual environment.

Main doorbell daemon:

```bash
python doorbell.py
```

Client to receive notifications:

```bash
python client.py
```

Make sure to specify the correct host to connect to in `config.py`. Also check
that the media player command is correct, or comment out the `check_call()` line
in `client.py` with a `#`.

Web logging server:

```bash
python log_server.py
```

There are also SystemD service installers:

```bash
sudo ./install_doorbell.sh # RPi side
```

```bash
sudo ./install_client.sh # Client side
```

```bash
sudo ./install_log_server.sh # Web log
```

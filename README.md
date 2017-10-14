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
Python 3.4+ (with venv and pip), `notify-send` and PostgreSQL 9.5-9.6.
Install those from your package manager if they are not installed already.

Clone or download:
```
git clone https://github.com/stephenangelico/Merrily.git
cd Merrily
```

Create virtual environment (recommended):
```
python3 -m venv env
source env/bin/activate
```

Install dependencies:
```
pip install -r requirements
pipenv install requests # pipenv installed by pip
```

Create database:
```
createdb merrily
```

Create a user for web interface:
```python
>>> import run
>>> run.adduser() # Follow the prompts then exit interpreter
```

Adjust `config.py` to your own needs.

Running
=======

This project is modular such that the doorbell backend is separate from the
server frontend. The two main files are doorbell.py and notifier.py, with helper
scripts for setting up databases and logins.

To run the server frontend:
```python run.py```

To run the doorbell backend:
```python merrily/doorbell.py```

`doorbell.py` is hard-coded to a particular host but in future this will become
localhost. To change the host the notification is sent to, simply adjust the
request line in `bell_ring()`.

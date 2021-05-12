#!/usr/bin/env python3
import os
import sys

# Static data
template = """[Unit]
Description=Merrily Doorbell (Module)
After=network.target

[Service]
Environment=
User=(User)
WorkingDirectory=(directory)
ExecStart=(Python) -u (scriptname.py)
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
"""
#Environment=VIRTUAL_ENV='`pwd`/env'
bits = {}

# Figure out what to install
if len(sys.argv) > 1:
	if sys.argv[1] == "client":
		bits["module"] = "Client"
		bits["script"] = "cyril.py"
		bits["display"] = True # TODO: set to current display
	elif sys.argv[1] == "server":
		bits["module"] = "Server"
		bits["script"] = "blanche.py"
	elif sys.argv[1] == "doorbell":
		bits["module"] = "Sensor"
		bits["script"] = "doorbell.py"
else:
	print("Please specify 'client', 'server' or 'doorbell'.")
	sys.exit()

# Check if we can/should install
if "SUDO_USER" in os.environ:
	bits["user"] = os.environ["SUDO_USER"]
else:
	print("This install script must be run using sudo.")
	sys.exit()

# Actually install

# Get directory of this script, which we will assume is in the same directory
# as all scripts to be installed
bits["directory"] = os.path.dirname(os.path.realpath(sys.argv[0]))
if "VIRTUAL_ENV" in os.environ:
	bits["virtualenv"] = os.environ["VIRTUAL_ENV"]
# If a Python other than the system Python runs this script, assume that
# Python is the one the user wants the services to be run with.
bits["python"] = sys.executable


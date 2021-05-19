#!/usr/bin/env python3
import os
import sys
#import argparse
#parser = argparse.ArgumentParser()
#parser.parse_args()

# Static data
template = """[Unit]
Description=Merrily Doorbell {module}
After=network.target

[Service]
Environment={environment}
User={user}
WorkingDirectory={directory}
ExecStart={python} -u {script}
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
"""
bits = {}

# Figure out what to install
if len(sys.argv) > 1:
	if sys.argv[1] == "client":
		bits["module"] = "Client"
		bits["script"] = "cyril.py"
		bits["service"] = "cyril.service"
	elif sys.argv[1] == "server":
		bits["module"] = "Server"
		bits["script"] = "blanche.py"
		bits["service"] = "blanche.service"
	elif sys.argv[1] == "doorbell":
		bits["module"] = "Sensor"
		bits["script"] = "doorbell.py"
		bits["service"] = "doorbell.service"
else:
	print("Please specify 'client', 'server' or 'doorbell'.")
	sys.exit()

# Check if we can/should install
#if os.getuid() == 0:
	

if "SUDO_USER" in os.environ:
	bits["user"] = os.environ["SUDO_USER"]
else:
	print("This install script must be run using sudo.")
	sys.exit()

# Actually install

# Get directory of this script, which we will assume is in the same directory
# as all scripts to be installed
bits["directory"] = os.path.dirname(os.path.realpath(sys.argv[0]))
# Use instance of Python used to install
bits["python"] = sys.executable

bits["environment"] = ""
for var in ["VIRTUAL_ENV", "DISPLAY"]:
	if var in os.environ:
		bits["environment"] += (var + "=" + os.environ[var] + " ")

service_file = template.format_map(bits)
print(service_file)

#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
parser = argparse.ArgumentParser(description="Install Merrily service files")
parser.add_argument("module", choices=['client', 'server', 'doorbell'], help="Merrily module to install")
parser.add_argument("-u", "--user", action="store", default=str(os.getuid()), help="User to run service as")
parser.add_argument("-n", "--dry-run", action="store_true", help="Print to screen only")
args = parser.parse_args()

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
if args.module == "client":
	bits["module"] = "Client"
	bits["script"] = "cyril.py"
	bits["service"] = "cyril.service"
elif args.module == "server":
	bits["module"] = "Server"
	bits["script"] = "blanche.py"
	bits["service"] = "blanche.service"
elif args.module == "doorbell":
	bits["module"] = "Sensor"
	bits["script"] = "doorbell.py"
	bits["service"] = "doorbell.service"

bits["user"] = args.user

# Get directory of this script, which we will assume is in the same directory
# as all scripts to be installed
bits["directory"] = os.path.dirname(os.path.realpath(sys.argv[0]))
# Use instance of Python used to install
bits["python"] = sys.executable

bits["environment"] = ""
for var in ["VIRTUAL_ENV", "DISPLAY"]:
	if var in os.environ:
		bits["environment"] += (var + "=" + os.environ[var] + " ")

# Actually install
service_file = template.format_map(bits)
if args.dry_run:
	print(service_file)
else:
	try:
		with open("/etc/systemd/system/%s" % bits["service"], mode="w") as f:
			f.write(service_file)
		subprocess.run(["systemctl", "--system", "daemon-reload"])
		subprocess.run(["systemctl", "enable", bits["service"]])
		subprocess.run(["systemctl", "start", bits["service"]])
		print("Installed as " + bits["service"] + ".")
	except PermissionError:
		escalate = input("Could not write service file. Would you like to run this as root?\n")
		if escalate[0] in ["Y", "y"]:
			os.execvp("sudo",
				(bits["environment"], sys.executable, os.path.realpath(sys.argv[0]), "-u", bits["user"], args.module))
		else:
			print("Aborted.")
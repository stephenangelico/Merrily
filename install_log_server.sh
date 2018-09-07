#!/bin/bash
# Install SystemD service for the hardware doorbell detector
instl ()
{ echo "[Unit]
Description=Merrily Log Server
After=network.target

[Service]
Type=simple
Environment=VIRTUAL_ENV='`pwd`/env'
User=$SUDO_USER
WorkingDirectory=`pwd`
ExecStart=`pwd`/env/bin/python3 -u `pwd`/log_server.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
" >/etc/systemd/system/merrily_log.service
systemctl --system daemon-reload
	systemctl enable merrily_log.service
	echo Installed as merrily_log.service.
	systemctl start merrily_log.service
}

if [[ `id -u` -ne 0 ]] ; then
	echo "This installer must be run using sudo."
	exit 1
fi
read -p "This will install log_server.py as a system service. Continue? [y/n] " -r
if [[ $REPLY =~ ^[Yy] ]] ; then
	instl
else
	echo "Aborted."
fi

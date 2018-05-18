#!/bin/bash
# Install SystemD service for the hardware doorbell detector
instl ()
{ echo "[Unit]
Description=Merrily Doorbell
After=network.target

[Service]
Type=simple
Environment=VIRTUAL_ENV='`pwd`/env'
User=`echo $SUDO_USER`
WorkingDirectory=`pwd`
ExecStart=`pwd`/env/bin/python3 `pwd`/doorbell.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
" >/etc/systemd/system/doorbell.service
systemctl --system daemon-reload
	systemctl enable doorbell.service
	echo Installed as doorbell.service.
	systemctl start doorbell.service
}

if [[ `id -u` -ne 0 ]] ; then
	echo "This installer must be run as root."
	exit 1
fi
read -p "This will install doorbell.py as a system service. Continue? [y/n] " -r
if [[ $REPLY =~ ^[Yy] ]] ; then
	instl
else
	echo "Aborted."
fi

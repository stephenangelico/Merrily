#!/bin/bash
# Install SystemD service for the hardware doorbell detector
instl ()
{ echo "[Unit]
Description=Doorbell Client
After=network.target

[Service]
Type=simple
Envirnment=VIRTUAL_ENV='/home/stephen/Merrily/env'
User=`stat -c %u $0`
WorkingDirectory=/home/stephen/Merrily
ExecStart=/home/stephen/Merrily/env/bin/python3 /home/stephen/Merrily/merrily/client.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
" >/etc/systemd/system/merrily.service
systemctl --system daemon-reload
	systemctl enable merrily.service
	echo Installed as merrily.service.
	systemctl start merrily.service
}

if [[ `id -u` -ne 0 ]] ; then
	echo "This installer must be run as root."
	exit 1
fi
read -p "This will install client.py as a system service. Continue? [y/n] " -r
echo # Create newline
if [[ $REPLY =~ ^[Yy] ]] ; then
	instl
else
	echo "Aborted."
fi

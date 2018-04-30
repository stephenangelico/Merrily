#!/bin/bash
# Install SystemD service for the hardware doorbell detector
instl ()
{ echo "[Unit]
Description=Merrily Doorbell
After=network.target

[Service]
Type=simple
Envirnment=VIRTUAL_ENV='/home/stephen/Merrily/env'
User=stephen
WorkingDirectory=/home/stephen/Merrily
ExecStart=/home/stephen/Merrily/env/bin/python3 /home/stephen/Merrily/merrily/doorbell.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
" >/etc/systemd/system/doorbell.service
systemctl --system daemon-reload
	systemctl enable doorbell.service
	echo Installed as doorbell.service.
	systemctl start doorbell.service
}

read -p "This will install doorbell.py as a system service. Continue? [y/n] " -r
echo # Create newline
if [[ $REPLY =~ ^[Yy] ]] ; then
	instl
else
	echo "Aborted."
fi
exit 0

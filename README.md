# Merrily
IP doorbell alert system
Named for the line in Gilbert and Sullivan's Princess Ida "Merrily ring the luncheon bell".

When someone presses the doorbell, a notification should pop up on any connected clients.

Client/server doorbell model:
Server listens to peripheral doorbell, sends JSON (?) packet to connected clients.
Clients may do any of: notify-send or system notification (inc Android), browser notification, browser flash, message in console

Maybe include a way to label a ring event to find when a thing happened?
Trigger may have to be written from scratch as well as server.
Worst case, get new doorbell or create one (need outdoor-rated shell) that can be connected

Version 1: RPi is client, server runs on "client" aka end user machine. Use notify-send.

Version 2: Add database log?
# Installation instructions:
0) The following should all be run as the user that will own the daemon process for sending alerts (should not be root)
1) Setup the message staging file:
1.1) `cp tmp.slack_warnings /tmp/slack_warnings`
2) Install the python dependencies all executables (you can choose to use a different location so long as you deal with absolute paths and $PATH correctly:
2.1) ``ln -s `pwd`/construct_body.py /usr/local/bin/construct_body``
2.2) ``ln -s `pwd`/slack_sender /usr/local/bin/slack_sender``
3) Update slack_sender.service with the user and working dir you want the daemon run under, and install it
3.1) `sudo cp ./slack_sender.service /etc/systemd/system/slack_sender.service`
3.2) `sudo cp ./etc.slack_sender /etc/slack_sender
3.3) `sudo systemctl daemon-reload`
4) Start the daemon and optionally enable it (so it runs automatically on boot):
4.1) `sudo systemctl start slack_sender`
4.2) (optional) `sudo systemctl enable slack_sender`
5) Make sure that your machine has a file /etc/fullname with the correct value

# Outstanding wishlist items
- Establish a configuration directory in /etc (/etc/slack_sender.d) that collects files with customizable messages for the various cases (\*.starts, \*.quits, \*.banters, others?)

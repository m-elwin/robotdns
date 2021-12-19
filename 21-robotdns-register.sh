#!/bin/sh
. ${CONNECTION_FILENAME}.settings
if [ "$2" = "up" ] || [ "$2" = "dhcp4-change" ]
then
    if [ "$CONNECTION_ID" = "${nmconnect}.robot" ] 
    then
        # Execute the ssh command as the original user
        su -c sh -c 'ssh -T -i $user_home/.ssh/id_robotdns robotdns@$dnshost' $(whoami) 
    fi
fi

#!/bin/sh

if [ "\$2" = "up" ] || [ "\$2" = "dhcp4-change" ]
then
    if [ "\$CONNECTION_ID" = "${nmconnect}.robot" ] 
    then
        # Execute the ssh command as the original user
        su -c sh -c 'ssh -T -i $HOME/.ssh/id_robotdns robotdns@$dnshost' $(whoami) 
    fi
fi

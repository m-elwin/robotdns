#!/bin/sh
echo "$(whoami)" > /tmp/foo
. ${CONNECTION_FILENAME}.settings
if [ "$2" = "up" ] || [ "$2" = "dhcp4-change" ]
then
    if [ "$CONNECTION_ID" = "${nmconnect}.robot" ] 
    then
        # Execute the ssh command as the original user
        ssh -T -o UserKnownHostsFile=$user_home/.ssh/known_hosts -i $user_home/.ssh/id_robotdns robotdns@$dnshost
    fi
fi

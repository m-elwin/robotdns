#!/bin/sh

# Network Manager Connection Profile to copy
nmconnect=$1

# hostname of the dns server
dnshost=$2

script=$(readlink -f "$0")
scriptpath=$(dirname "$script")

echo "Setting up Client. Profile: $nmconnect, Host: $dnshost"

# Delete the old key, make the new key
if [ -f ~/.ssh/id_robotdns ]
then
    echo "~/.ssh/id_robotdns already exists. Not creating new key. rm ~/.ssh/id_robotdns ~/.ssh/id_robotdns.pub and re-run to recreate key"
else
    echo "Creating ssh key: ~/.ssh/id_robotdns and ~/.ssh/id_robotdns.pub"
    ssh-keygen -t ed25519 -C $(hostname) -f ~/.ssh/id_robotdns -q -N ""
fi

echo "\nSend ~/.ssh/id_robotdns.pub to your system administrator to obtain access to the dns server"

dnsip=$(host $dnshost | grep -v IPv6 | awk '{ print $4 }')

nmcli con clone $nmconnect ${nmconnect}.robot
nmcli con mod ${nmconnect}.robot ipv4.dns-search msr 
nmcli con mod ${nmconnect}.robot ipv4.ignore-auto-dns true
nmcli con mod ${nmconnect}.robot ipv4.dns $dnsip

# Create the network manager startup script and
echo "Creating the network manager dispatch script:"
sudo cp ${scriptpath}/21-robotdns-register.sh /etc/NetworkManager/dispatcher.d/21-robotdns-register.sh
sudo chmod 500 /etc/NetworkManager/dispatcher.d/21-robotdns-register.sh

# Setup settigns for the user script to use
cat <<EOF | sudo tee /etc/NetworkManager/system-connections/${nmconnect}.robot.nmconnection.settings
export nmconnect=${nmconnect}
export dnshost=${dnshost}
export user_home=${HOME}
EOF
sudo chmod 600 /etc/NetworkManager/system-connections/${nmconnect}.robot.nmconnection.settings


echo "Complete. Use nmcli con up ${nmconnect}.robot to connect"

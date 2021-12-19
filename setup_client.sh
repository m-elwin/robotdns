#!/bin/sh

# Network Manager Connection Profile to copy
nmconnect=$1

# hostname of the dns server
dnshost=$2

echo "Profile: $nmconnect, Host: $dnshost"

# Delete the old key, make the new key
rm ~/.ssh/id_robotdns ~/.ssh/id_robotdns.pub
ssh-keygen -t ed25519 -C $(hostname) -f ~/.ssh/id_robotdns -q -N ""

echo "\nSend ~/.ssh/id_robotdns.pub to your system administrator to obtain access to the dns server"

dnsip=$(host $dnshost | grep -v IPv6 | awk '{ print $4 }')

nmcli con clone $nmconnect ${nmconnect}.robot
nmcli con mod ${nmconnect}.robot ipv4.dns-search msr 
nmcli con mod ${nmconnect}.robot ipv4.ignore-auto-dns true
nmcli con mod ${nmconnect}.robot ipv4.dns $dnsip


# Create the network manager startup script and
echo "Creating the network manager dispatch script:"
cat <<EOF | sudo tee /etc/NetworkManager/dispatcher.d/21-robotdns-register.sh
#!/bin/sh

if [ "\$2" = "up" ] || [ "\$2" = "dhcp4-change" ]
then
    if [ "\$CONNECTION_ID" = "${nmconnect}.robot" ] 
    then
        # Execute the ssh command as the original user
        su -c sh -c 'ssh -T -i $HOME/.ssh/id_robotdns robotdns@$dnshost' $(whoami) 
    fi
fi

EOF
sudo chmod 500 /etc/NetworkManager/dispatcher.d/21-robotdns-register.sh


echo "Complete. Use nmcli con up ${nmconnect}.robot to connect"

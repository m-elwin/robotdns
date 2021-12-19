#!/bin/sh

# Network Manager Connection Profile to copy
nmconnect=$1

# hostname of the dns server
dnshost=$2

ssh-keygen -t ed25519 -C $(hostname) -f ~/.ssh/id_robotdns

echo "Send ~/.ssh/id_robotdns.pub to your system administrator to obtain access to the dns server"

dnsip=$(host $serv_host | grep -v IPv6 | awk '{ print $4 }')

nmcli con clone $nmconnect ${nmconnect}.robot
nmcli con mod $nmconnect.robot ipv4.dns-search msr 
nmcli con mod $nmconnect.robot ipv4.ignore-auto-dns true
nmcli con mod $nmconnect.robot ipv4.dns $dnsip


# Create the network manager startup script

cat <<EOF | sudo tee /etc/NetworkManager/dispatcher.d/21-robotdns-register.sh
#!/bin/sh

if [ "$2" = "up" ] || [ "$2" = "dhcp4-change" ]
then
    if [ "$CONNECTION_ID" = "${nmconnect}.robot}" ] 
    then
        ssh robotdns@$dnshost
    fi
fi

EOF

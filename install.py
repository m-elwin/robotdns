#!/usr/bin/env python3


def setup_dnsmasq(dns1, dns2):
"""
   Configure /etc/dnsmasq.conf for use with robotdns
"""
    # Here are the options that are changed by default for the robotdns project
    # Upstream DNS servers
#    server=129.105.1.1
#    server=129.105.49.1

    # User and group that dnsmasq runs as
#    user=robotdns
#    group=robotdns

    # We don't want to read from the system's hosts file
#    no-hosts

    # This directory is where the clients register themselves 
#    addn-hosts=/home/robotdns/hosts/

    # These two options enable us to NOT use fully qualified names
#    expand-hosts
#    domain=msr



if __name__ == "__main__":
    # Step 1, create the user (if it does not exist)
    # Step 2, configure DNS 

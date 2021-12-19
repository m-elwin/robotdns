#!/usr/bin/env python3
"""
 Enables the user to register/unregister their hostname and IP address with the DNS server
"""

import sys
import os

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Must provide a host")
        sys.exit(1)

    host = sys.argv[1]
    # get the client ip address.  this works because we are assuming everyone is on the same corporate LAN
    client = os.environ.get("SSH_CLIENT")
    client_ip = client.split(" ")[0]

    # Update the ip address entry for the host
    with open(f"/home/robotdns/{host}","w") as hosts:
            print(f"{client_ip} {host}", file=hosts)

    # Refresh dnsmasq
    with open("/run/dnsmasq/dnsmasq.pid") as dnsmasq_pid:
            os.kill(dnsmasq_pid, signal.SIGHUP)



#!/usr/bin/env python3
"""
 Enables the user to register/unregister their hostname and IP address with the DNS server
"""

if __name__ == "__main__":
    # register hostname ip
    # unregister hostname
    
    @cherrypy.expose
    def register_dns(self, ip, host):
        """ Directly get the ca cert. assumes it has already been issued """
        with open(f"/home/dns/hosts/{host}","w") as hosts:
            print(f"{ip} {host}", file=hosts)
        with open("/run/dnsmasq/dnsmasq.pid") as dnsmasq_pid:
            os.kill(dnsmasq_pid, signal.SIGHUP)
        return "Success"



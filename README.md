# Overview
Robot DNS is a dynamic DNS server for a very specific robotics application:

1. Every robot connects to the same local network, as do the robot users
2. You do not control the local network, but do control a server on that network 
3. You want every robot and every user to be able to contact each other by hostname
4. You do not want to use mDNS, or it does not work (see 2)

# Server Installation
## RobotDNS User Setup
1. Create a new user called `robotdns`. For example: `useradd -m robotdns`.
2. In the `robotdns` home directory, `git clone https://github.com/m-elwin/robotdns.git`
3. To provide a user access, obtain their public ssh key.
   - `~/robotdns/robot_users.py --add <keyfile.pub> hostname` to add the user's key.
   - Each key is tied to exactly one hostname. 
4. To remove a client use `~/robotdns/robot_users.py --rm hostname`
   
## Install and Configure dnsmasq
1. `sudo apt install dnsmasq`
2. Add the following options to `/etc/dnsmasq.conf` 
   ```
   #/etc/dnsmasq.conf
   # Upstream DNS server ip addresses (whatever your network uses)
   server=111.222.333.444
   server=555.666.777.888

   # User and group that dnsmasq runs as (e.g., robotdns)
   user=robotdns
   group=robotdns

   # Don't read from the system's hosts file (your setup may vary)
   no-hosts

   # This directory is where the clients register themselves 
   addn-hosts=/home/robotdns/hosts/

   # These two options enable us to NOT use fully qualified names
   # Which is not necessary but
   expand-hosts
   domain=msr # can be anything that is not an actual TLD (e.g., com, org, edu) 
   ```
3. Enable and start `dnsmasq`: `systemctl enable --now dnsmasq`

# Client Installation
1. The client must have ssh access to the `robotdns` user via a public key
   - Users can, for example, generate keys with `ssh-keygen -t ed25519`. The public key is then stored in `~/.ssh/id_ed25519.pub`
2. Users should download the installation script:
   `scp robotdns@<server>:/home/roboddns/robotdns/install_robot.py /tmp/install_robot.py`
3. Run the one-time installation: 
   `/tmp/install_robot.py <nmconnection> <server>`, where `<nmconnection>` is the name of the Network Manager connection that connects
   to the network that the robots are on and `<server>` is the hostname of the dns server.
3. `nmcli con up <nmconnection>.robot` connects to the robot network using the `robotdns` server and registers your computer
   with that server. It is recommended to only connect to this network when using the robots

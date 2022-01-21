# Overview
Robot DNS is a dynamic DNS server for a very specific robotics application:

1. Every robot connects to the same local network, as do the robot users
2. You do not control the local network, but do control a server on that network 
3. You want every robot and every user to be able to contact each other by hostname
4. You do not want to use mDNS, or it does not work (see 2)

# Server Installation
## RobotDNS User Setup
1. Create a new user called `robotdns`. For example: `useradd -m robotdns`.
2. Create `/home/robotdns/hosts`: `mkdir -p /home/robotdns/hosts`
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
   # This is important for ROS since some parts of it expect hostname to resolve directly
   expand-hosts

   # The domain is fixed at msr (otherwise you need to modify the client-side script)
   domain=msr
   ```
2. Disable systemd-resolved: `systemctl disable --now systemd-resolved`
3. Enable and start `dnsmasq`: `systemctl enable --now dnsmasq`

# Client
## Installation
1. Download and run the installation script:
   - `curl -L "https://raw.githubusercontent.com/m-elwin/robotdns/main/setup_client.sh" | sh -s -- <profile> <server>`, where `<profile>` is the name of the network manager profile (usually the wifi network name) to clone
      and `<server>` is the address of the robotdns server (provided by the system administrator)
   - The script will create an ssh key. The public key (ending in `.pub`) should be sent to your system administrator and is used to grant access. 
   - If you are concerned about running the script, view it first!
   - The private key should be kept secret. Anyone with your private key can associate your hostname with any ip address on the server.
1. After your administrator has provided access, run `ssh -T -i $HOME/.ssh/id_robotdns robotdns@<server>` to verify the connection.
   - This will prompt you to accept a fingerprint.
   - Your administrator will provide you with what fingerprint to expect. This should match what you see to verify that you have
     connected to the correct server..
## Usage
3. `nmcli con up <nmconnection>.robot` connects to the robot network using the `robotdns` server and registers your computer
   - Assuming your ssh-keys are added to the agent automatically, this will automatically register you
   - If not, you can manually do `ssh add ~/.ssh/id_robotdns` to add your key prior to connecting

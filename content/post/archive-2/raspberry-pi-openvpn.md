---
title: raspberry pi openvpn
author: "-"
date: 2017-08-30T14:34:17+00:00
url: /?p=11072
categories:
  - Raspberry-Pi
tags:
  - reprint
---
## raspberry pi openvpn
<https://community.home-assistant.io/t/how-to-install-openvpn-on-raspberry-pi-with-home-assistant/59002>

```bash
sudo -s  #  **rest of the instructions assume you've already done this
apt-get update
apt-get upgrade

apt-get install openvpn unzip easy-rsa
gunzip -c /usr/share/doc/openvpn/examples/sample-config-files/server.conf.gz > /etc/openvpn/server/server.conf

vim /etc/openvpn/server/server.conf
```

> Make the following changes to the server.conf file
> Increase key security by Finding dh and makesure it reads dh dh2048.pem
> Allow web traffic pass though to client by uncommenting push "redirect-gateway def1 bypass-dhcp" by removing the semi colon at the start of the line
> Prevent DNS leak by overriding the default DNS - Uncomment push "dhcp-option DNS 208.67.222.222" and push "dhcp-option DNS 208.67.220.220"
> Lower OpenVPNs run time auth - Uncomment user nobody and group nogroup
> Change the port OpenVPN runs on it should current by port 1194 - choose something obscure and above 1024 e.g. port 50000 - leave it as UDP
> Now save your changes and exit.

Enable Packet Forwarding

```bash
bash -c 'echo 1 > /proc/sys/net/ipv4/ip_forward'

# Make this change perminant by un-commenting net.ipv4.ip_forward=1
vim /etc/sysctl.conf

cp -r /usr/share/easy-rsa/ /etc/openvpn

mkdir /etc/openvpn/easy-rsa/keys
vim /etc/openvpn/easy-rsa/vars
#Change the below to something more relevant to your region

export KEY_COUNTRY="US"
export KEY_PROVINCE="TX"
export KEY_CITY="Dallas"
export KEY_ORG="My Company Name"
export KEY_EMAIL="sammy@example.com"
export KEY_OU="MYOrganizationalUnit"

Change
export KEY_NAME="EasyRSA"
to
export KEY_NAME="server"

Save the file

Generate the Server Cert - this takes a very long time (my Pi took 2 hours)

openssl dhparam -out /etc/openvpn/dh2048.pem 2048

CD to the easy-dir
cd /etc/openvpn/easy-rsa

type sudo su to swithc to root

Run the following command (copy exactly)
source ./vars

Run this command to fix the bug with Easy RSA
sudo cp openssl-1.0.0.cnf openssl.cnf

Run this command to clean up
./clean-all

Run this command to build the ca - bypass the prompts as you already set the values in vars

Generate a Certificate and Key for the Server
./build-ca
While working in /etc/openvpn/easy-rsa
./build-key-server server
Bypass the values again - but this time you will be asked for a password - leave this blank

Final two questions will be
Sign the certificate? [y/n]

1 out of 1 certificate requests certified, commit? [y/n]

Answer yes to both

Copy the new certs to the OpenVPN folder
cp /etc/openvpn/easy-rsa/keys/{server.crt,server.key,ca.crt} /etc/openvpn

Verfiy the files are copied ls /etc/openvpn

Ready to start your OpenVPN server!!

exit root mode by pressing ctrl+d and run

`sudo service openvpn start`
`sudo service openvpn status`
All being well you should see Active: active (exited) since…

Client Cert Generation

Now you have a fully working OpenVPN server its time to generate some client certificates. You can generate one per user - but the key here is that without a cert they cant connect to your VPN

Working out of /etc/openvpn/easy-rsa

Run the following one by one
sudo su
source ./vars
./build-key client1

Leave the prompts blank - and decide if you want a challenge password on the cert (I'd advise setting one, because if your CERT fell in to the wrong hands - they would need the password to use it.)

Copy the sample client config to the easy rsa folder
cp /usr/share/doc/openvpn/examples/sample-config-files/client.conf /etc/openvpn/easy-rsa/keys/client.ovpn

Edit the client config
nano /etc/openvpn/easy-rsa/keys/client.ovpn

First thing to change is you need to put the public IP or public DNS of your internet here (you can get a dynamic DNS setup if your internet IP changes) - also note the port number you set open VPN to run on

remote your_server_ip 50000

Again uncomment

user nobody
group nogroup

Ok - that's it - you just setup your OpenVPN server, generated a server cert, a server key and a client side key, cert and config

The client cert, key and config are all part of the package that needs to be deployed to the client (On an iPhone you would need to use iTunes to copy these files over)

client1.crt
client1.key
client.ovpn
ca.crt

If your struggling with the multiple files - I would suggest combining the client1.crt, client1.key and ca.crt into the ovpn file and then just deploying the one file to the device

To combine the files into a unified file (unified ovpn file)

Edit client.ovpn

Comment the following by adding a ; in front of each line
;ca ca.crt
;cert client.crt
;key client.key

Save the file and run the follow three commands
echo '<ca>' >> /etc/openvpn/easy-rsa/keys/client.ovpn
cat /etc/openvpn/ca.crt >> /etc/openvpn/easy-rsa/keys/client.ovpn
echo '</ca>' >> /etc/openvpn/easy-rsa/keys/client.ovpn

Run these 3 commands
echo '<cert>' >> /etc/openvpn/easy-rsa/keys/client.ovpn
cat /etc/openvpn/easy-rsa/keys/client1.crt >> /etc/openvpn/easy-rsa/keys/client.ovpn
echo '</cert>' >> /etc/openvpn/easy-rsa/keys/client.ovpn

Run these 3 commands
echo '<key>' >> /etc/openvpn/easy-rsa/keys/client.ovpn
cat /etc/openvpn/easy-rsa/keys/client1.key >> /etc/openvpn/easy-rsa/keys/client.ovpn
echo '</key>' >> /etc/openvpn/easy-rsa/keys/client.ovpn

If you run cat /etc/openvpn/easy-rsa/keys/client.ovpn you will see the 3 files have been appended to the client ovpn file

7.You now have one client.ovpn file that when you deploy it to your device - with the OpenVPN app you can VPN into your home network.

See https://nordvpn.com/tutorials/android/openvpn/ 1 for more help on how to deploy ovpn files to your device

WARNING: DO NOT UNDER ANY CIRCUMSTANCE let these OVPN Client files get into the wrong hands, don't email them to your device, only use trusted methods to copy them over. Remember with this file (and your challenge key if you set one) anyone could connect to your VPN

Once these files are on your remote device open port 50000 to on your router to your Pi

Consider setting up fail2ban for open VPN (this will ban IPs that try to connect to OpenVPN at port 50000) But with out a the above client config file - they are kind of wasting their time.


-------

```

<https://www.raspberrypi.org/forums/viewtopic.php?t=81657>

```bash
iptables -A INPUT -i tun+ -j ACCEPT
iptables -A OUTPUT -o tun+ -j ACCEPT
iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o wlan0 -j MASQUERADE
iptables -I FORWARD -i tun0 -o wlan0 -s 10.8.0.0/24 -d 192.168.1.0/24 -m conntrack --ctstate NEW -j ACCEPT
iptables -A INPUT -i wlan0 -m state --state NEW -p udp --dport 4911 -j ACCEPT
iptables -A FORWARD -i tun+ -j ACCEPT
iptables -A FORWARD -i tun+ -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i wlan0 -o tun+ -m state --state RELATED,ESTABLISHED -j ACCEPT
service openvpn restart

```

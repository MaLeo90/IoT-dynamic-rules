# CyberIntelligence For IoT Requisites

These are scripts for installing and starting the tools that support the IoT sentinel. 

The requisites of executing these scripts are:

- The operating system must be [Ubuntu 16.04 TLS](https://www.ubuntu.com/download/desktop) for desktop and [Ubuntu Mate 16.04 TLS](https://ubuntu-mate.org/download/) for Raspberry pi 3
- The username must be "sentinel"
- You need sudo privileges
- Your Ethernet net card must allow promiscous mode
- Your Wifi net card must allow monitor mode

Before running the installing script be sure you changed the ip in the line "\*.local5@10.10.3.198:514" in the file rsyslog.conf to the ip of your OSSIM instance.

To install all the requisites and download the sentinel run: ```sudo ./setup.sh```. The programs installed and downloaded are:

- Radare2
- Yara 3.7.1 (With R2Yara)
- Suricata 4.0 (With file extraction and syslog events)
- IoT Sentinel Python Modules
- OpenVas 8
- Kismet

After installing the sentinel run ```sudo nano /etc/kismet/kismet.conf```. In this file uncomment the line "ncsource=wlan0" and change "wlan0" to your wifi interface.

To run Suricata use:
```sudo ./suricata-start.sh <your_net_interface>```

To run kismet use:
```sudo ./kismet-start.sh <your_net_interface>``` where the interface is the same you defined in kismet.conf

Tested on Ubuntu 16.04 LTS and Ubuntu Mate IoT 16.04

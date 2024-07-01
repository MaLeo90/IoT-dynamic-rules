#!/bin/sh

#Update and upgrade
apt-get update && apt-get upgrade -y
#Dependencies install
apt-get install -y automake libtool make gcc libssl-dev libjansson-dev python3 python3-pip ethtool unzip sqlite3 software-properties-common libfreetype6-dev pkg-config libpng12-dev chromium-browser

#Radare2
cd  ..
#git clone https://github.com/radare/radare2
wget https://github.com/radare/radare2/archive/2.5.0.zip
unzip 2.5.0.zip
cd radare2-2.5.0
sys/install.sh
cd ..
#Yara
chmod 777 -R CyberIntelligenceForIoTRequisites
cd CyberIntelligenceForIoTRequisites
wget https://github.com/VirusTotal/yara/archive/v3.7.1.zip
unzip v3.7.1.zip
chmod 777 -R yara-3.7.1
rm yara-3.7.1/Makefile.am yara-3.7.1/libyara/Makefile.am yara-3.7.1/configure.ac yara-3.7.1/libyara/modules/module_list
cp YaraFiles/Makefile.am yara-3.7.1 
cp YaraFiles/configure.ac yara-3.7.1 
cp YaraFiles/libyara/Makefile.am yara-3.7.1/libyara/Makefile.am 
cp YaraFiles/libyara/modules/module_list yara-3.7.1/libyara/modules/ 
cp YaraFiles/libyara/modules/r2.c yara-3.7.1/libyara/modules/
cp YaraFiles/libyara/modules/androguard.c yara-3.7.1/libyara/modules
cd yara-3.7.1
./bootstrap.sh
./configure --enable-cuckoo
make
make install
#Suricata
cd ..
add-apt-repository -y ppa:oisf/suricata-stable
apt-get update
apt-get install -y suricata 
#mkdir /var/log/suricata
#mkdir /etc/suricata
rm /etc/suricata/suricata.yaml
rm /etc/rsyslog.conf
cp rsyslog.conf /etc
cp suricata.yaml /etc/suricata
cp file-extract.rules /etc/suricata/rules
#Sentinel
pip3 install pymisp
pip3 install androguard[magic,graphing,GUI]
pip3 install pyfcm
#Openvas host: https://localhost:4000 admin:admin
apt update && sudo apt upgrade -y
add-apt-repository -y ppa:mrazavi/openvas
apt update
apt install openvas9 -y
apt install libopenvas9-dev
greenbone-nvt-sync
greenbone-scapdata-sync
greenbone-certdata-sync
systemctl restart openvas-scanner
systemctl restart openvas-manager
systemctl restart openvas-gsa
systemctl enable openvas-scanner
systemctl enable openvas-manager
systemctl enable openvas-gsa
wget --no-check-certificate https://svn.wald.intevation.org/svn/openvas/branches/tools-attic/openvas-check-setup -P /usr/local/bin/
chmod +x /usr/local/bin/openvas-check-setup
openvas-check-setup --v9
openvasmd --rebuild --progress
#Kismet
apt-get update
apt-get install -y kismet

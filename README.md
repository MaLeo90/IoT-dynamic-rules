Before starting the sentinel you must configure all parameters on "keys.py" unless it may fail in the execution

To start the sentinel just execute ```python3 suricata_read.py```, this will start monitoring "objects" and when suricata sends some file in there it will be catched and analyzed.

To use the "experiments.py" file you will need a server with 100 samples, 50 goodware and 50 malware. Start a sniffer and execute ```python3 experiments.py```. When the downloads finished save the pcap so you can use it with tcpreplay.

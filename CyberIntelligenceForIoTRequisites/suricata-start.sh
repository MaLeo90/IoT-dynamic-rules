#!/bin/sh

INTERFACE=$1

ethtool -K $INTERFACE tso off
ethtool -K $INTERFACE gro off
ethtool -K $INTERFACE lro off
ethtool -K $INTERFACE gso off
ethtool -K $INTERFACE rx off
ethtool -K $INTERFACE tx off
ethtool -K $INTERFACE sg off
ethtool -K $INTERFACE rxvlan off
ethtool -K $INTERFACE txvlan off

suricata -c /etc/suricata/suricata.yaml -i $INTERFACE --init-errors-fatal

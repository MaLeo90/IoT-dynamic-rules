#!/bin/sh

INTERFACE=$1

ifconfig $INTERFACE down
iwconfig $INTERFACE mode monitor
ifconfig $INTERFACE up

kismet

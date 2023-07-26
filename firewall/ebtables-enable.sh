#!/bin/bash

# Flush existing rules and set default policies to DROP
ebtables -F
ebtables -P INPUT DROP
ebtables -P FORWARD DROP
ebtables -P OUTPUT DROP

# Allow incoming and outgoing traffic with Ethertype 0x88e5 (MACSec)
ebtables -A INPUT -p 0x88e5 -j ACCEPT
ebtables -A OUTPUT -p 0x88e5 -j ACCEPT




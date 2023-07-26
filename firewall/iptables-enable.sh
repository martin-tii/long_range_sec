#!/bin/bash

# Flush existing rules and set default policies to DROP
iptables -F
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

# Allow incoming and outgoing traffic with Ethertype 0x88e5 (MACSec)
iptables -A INPUT -m ethertype --ethertype 0x88e5 -j ACCEPT
iptables -A OUTPUT -m ethertype --ethertype 0x88e5 -j ACCEPT


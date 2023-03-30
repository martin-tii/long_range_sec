#!/bin/bash
### This command should be executed as ./test.sh <interface> <primary/secondary>
### primary means the first node that will be running (will get the key1
###

key1="12345678901234567890123456789012" #key on one side
key2=$(echo "$key1" | rev); # reversing the key on the other side, for testing

get_mac()
{
echo "$(ip -brief link | grep "$1" | awk '{print $3; exit}')"
}

down()
{
mac=$(get_mac "$1")
ip link del link "$1" macsec0 type macsec encrypt on
}

up()
{
mac=$(get_mac "$1")
ip link add link "$1" macsec0 type macsec encrypt on
ip macsec add macsec0 rx port 1 address "$mac"
if [[ "$2" == "primary" ]]
then
  ip macsec add macsec0 tx sa 0 pn 1 on key 01 "$key1"
  ip macsec add macsec0 rx port 1 address "$mac" sa 0 pn 1 on key 00 "$key2"
else
  ip macsec add macsec0 tx sa 0 pn 1 on key 01 "$key2"
  ip macsec add macsec0 rx port 1 address "$mac" sa 0 pn 1 on key 00 "$key1"
fi
ip link set macsec0 up
ipa=$(( ( RANDOM % 100 )  + 1 ))
ip addr add 10.10.10."$ipa"/24 dev macsec0
echo "IP: 10.10.10.$ipa/24"
}


if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit
  else
      if [ "$1" == "down" ]
      then
         down "$2"
     fi
     if [ "$1" == "up" ]
     then
        up "$2" "$3"
fi


fi

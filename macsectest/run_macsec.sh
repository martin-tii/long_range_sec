#!/bin/bash
### This command should be executed as ./run_macsec.sh <up/down> <interface> <primary/secondary>
### up is to set the interface up
### primary means the first node that will be running (will get the key1
###
#!/bin/bash

configure_mac_sec()
{

  echo "configuring MacSec"

  source variables.conf
        interface=$INTERFACE
        status=$STATUS
        role=$ROLE
        key1=$KEY1
        #key2=$(echo "$key1" | rev);
        key2=$KEY2
        macprim=$MACPRIM
        macseco=$MACSECO

  get_mac()
  {
  echo "$(ip -brief link | grep "$interface" | awk '{print $3; exit}')"
  }

  down()
  {
  echo "$interface"
  mac=$(get_mac "$interface")
  ip link del link "$interface" macsec0 type macsec encrypt on
  }

  up()
  {
  echo "here"
  ip link set "$interface" up
  ip link add link "$interface" macsec0 type macsec encrypt on

  if [[ "$role" == "primary" ]]
  then
    ip macsec add macsec0 tx sa 0 pn 1 on key 01 "$key1"
    ip macsec add macsec0 rx port 1 address "$macseco"
    ip macsec add macsec0 rx port 1 address "$macseco" sa 0 pn 1 on key 02 "$key2"
  else
    ip macsec add macsec0 tx sa 0 pn 1 on key 01 "$key2"
    ip macsec add macsec0 rx port 1 address "$macprim"
    ip macsec add macsec0 rx port 1 address "$macprim" sa 0 pn 1 on key 02 "$key1"
  fi
  ip link set macsec0 up
  ipa=$(( ( RANDOM % 100 )  + 1 ))
  ip addr add 10.10.10.$ipa/24 dev macsec0
  echo "IP: 10.10.10.$ipa/24"
  }


  if [ "$status" == "down" ]
     then
     down "$interface"
  fi
  if [ "$status" == "up" ]
    then
    up "$interface"
  fi
}


configure_mac_sec
ip macsec show

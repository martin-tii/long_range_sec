ip link add link eth0 macsec0 type macsec
ip macsec add macsec0 tx sa 0 pn 1 on key 02 09876543210987654321098765432109
ip macsec add macsec0 rx address 56:68:a5:c2:4c:14 port 1
ip macsec add macsec0 rx address 56:68:a5:c2:4c:14 port 1 sa 0 pn 1 on key 01 12345678901234567890123456789012
ip link set dev macsec0 up
ifconfig macsec0 10.10.12.2/24

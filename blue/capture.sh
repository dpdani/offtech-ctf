#!/usr/local/bin/bash

#set -x # echo on

EXPERIMENT="ctf-resilient-g3"
SERVER="server.${EXPERIMENT}.offtech"
FILENAME="capture"
DST_IP="10.1.2.2"

ETH=$(ssh ${SERVER} "sudo ip route get ${DST_IP}" | head -1 | awk '{print $5}')

ssh ${SERVER} "sudo tcpdump -s0 -U --immediate-mode -nn -i ${ETH} -w ~/CCTF-Resilient-Server/blue/pcap.pcap"

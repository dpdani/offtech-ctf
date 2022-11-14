#!/usr/local/bin/bash

#set -x # echo on

EXPERIMENT="ctf-resilient-g3"
DST_IP="10.1.2.2"

ETH=$(ssh $1.${EXPERIMENT}.offtech "sudo ip route get ${DST_IP}" | head -1 | awk '{print $5}')

rm -f "~/offtech-ctf/blue/pcap.pcap"
ssh $1.${EXPERIMENT}.offtech "sudo tcpdump -s0 -U --immediate-mode -nn -i ${ETH} -w ~/offtech-ctf/blue/pcap.pcap"


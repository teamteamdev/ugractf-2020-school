#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools

from scapy.layers.inet import IP
from scapy.utils import rdpcap


def solve():
    dump = rdpcap('hello.pcap')

    byte = 0
    answer = bytearray()

    for i, packet in zip(itertools.count(), dump):
        flag = (packet[IP].flags >> 2) & 1
        byte = (byte << 1) | flag

        if i % 8 == 7:
            answer.append(byte)
            byte = 0
    
    print(answer.decode())


if __name__ == "__main__":
    solve()

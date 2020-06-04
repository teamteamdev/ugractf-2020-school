#!/usr/bin/env python3

import copy
import hmac
import json
import os
import random
import sys

from scapy.layers.inet import IP, UDP
from scapy.utils import rdpcap, wrpcap


PREFIX = "ugra_this_bit_is_r5s5rv5d_"
SECRET = b"deviation-hiccup-understandings-strange-scan"
SALT_SIZE = 10

def get_flag():
    user_id = sys.argv[1]
    return PREFIX + hmac.new(SECRET, str(user_id).encode(), "sha256").hexdigest()[:SALT_SIZE]


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)
    
    random.seed(sys.argv[1])
    
    flag = get_flag()
    flag_bits = ''.join(f"{i:08b}" for i in flag.encode())

    target_dir = sys.argv[2]

    sample = rdpcap('private/template.pcap')[0]

    last_id = random.randint(1, 40968)
    last_sport = random.randint(16384, 25632) * 2
    last_time = 1590000000 + random.uniform(0, 10000000)

    dump = []
    for bit in flag_bits:
        packet = copy.deepcopy(sample)
        dump.append(packet)

        packet.time = last_time
        last_time += random.uniform(1, 1.0001)

        packet[IP].id = last_id
        last_id += 1
        packet[IP].flags |= 4 * (bit == '1')
        packet[IP].chksum = None

        packet[UDP].sport = last_sport
        last_sport += 2
        packet[UDP].chksum = None
    
    wrpcap(os.path.join(target_dir, "hello.pcap"), dump)
    
    json.dump({"flags": [flag]}, sys.stdout)


if __name__ == "__main__":
    generate()

#!/usr/bin/env python3

import hmac
import json
import os
import random
import sys

PREFIX = "ugra_deified_civic_radar_reviver_"
SECRET = b"kayak-racecar-madam-refer-redivider"
SALT_SIZE = 12

def get_flag():
    user_id = sys.argv[1]
    return PREFIX + hmac.new(SECRET, str(user_id).encode(), "sha256").hexdigest()[:SALT_SIZE]


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)
    user_id = sys.argv[1]
    target_dir = sys.argv[2]

    flag = get_flag()

    random.seed(hmac.new(SECRET, str(user_id).encode(), "sha256").digest())

    words = [flag] + ["".join([random.choice("asdfhjklqweruiop") for _ in range(random.randint(7, 20))])
                      for _ in range(random.randint(9, 15))]
    random.shuffle(words)
    text = " ".join(words)
    bits = "".join([f"{i:08b}" for i in text.encode()])
    bits = bits[::-1]

    open(os.path.join(target_dir, "reverse.txt.bin"), "wb").write(int(bits, 2).to_bytes(len(bits) // 8, "big"))

    json.dump({
        "flags": [flag],
        "substitutions": {},
        "urls": []
    }, sys.stdout)


if __name__ == "__main__":
    generate()

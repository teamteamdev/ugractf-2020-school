#!/usr/bin/env python3

import gzip
import hmac
import json
import os
import random
import sys

PREFIX = "ugra_mind_your_updates_"
SECRET = b"paste-define-attraction-desperate-juxtaposition"
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

    flag_str = " || ".join(random.choice(["'%s'" % c, "x'%02x'" % ord(c)]) for c in flag)

    dump = gzip.open(os.path.join("private", "dump.sql.gz")).read()
    dump = dump.replace(b"+++flag+++", flag_str.encode())
    gzip.open(os.path.join(target_dir, "db-dump.sql.gz"), "wb").write(dump)

    json.dump({"flags": [flag], "substitutions": {}, "urls": []}, sys.stdout)


if __name__ == "__main__":
    generate()

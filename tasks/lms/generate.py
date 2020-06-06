#!/usr/bin/env python3

import hmac
import json
import os
import shutil
import subprocess
import sys
import tempfile

PREFIX = "ugra_use_well_tested_sandboxes_"
SECRET1 = b"carried thy soldier have"
SALT1_SIZE = 16
SECRET2 = b"order many pair dream"
SALT2_SIZE = 12


def get_user_tokens():
    user_id = sys.argv[1]

    token = hmac.new(SECRET1, str(user_id).encode(), "sha256").hexdigest()[:SALT1_SIZE]
    flag = PREFIX + hmac.new(SECRET2, token.encode(), "sha256").hexdigest()[:SALT2_SIZE]

    return token, flag


def generate():
    if len(sys.argv) < 3:
        print("Usage: generate.py user_id target_dir", file=sys.stderr)
        sys.exit(1)

    token, flag = get_user_tokens()

    json.dump({
        "flags": [flag],
        "substitutions": {},
        "urls": [f"https://lms.{{hostname}}/{token}/"]
    }, sys.stdout)


if __name__ == "__main__":
    generate()

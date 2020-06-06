#!/usr/bin/env python3

import hmac
import json
import os
import random
import sys
import zipfile

PREFIX = "ugra_slowly_losing_bits_of_sanity_"
SECRET = b"duck-swallow-finch-mesh-origami"
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
            
    deletions = {i: [] for i in "abcdefghijklmnopqrstuvwxyz0123456789_"}
    for n, c in enumerate(flag):
        deletions[c].append(n)

    z = zipfile.ZipFile(os.path.join("private", "document.docx"))
    z_target = zipfile.ZipFile(os.path.join(target_dir, "printme.docx"), 'w', zipfile.ZIP_DEFLATED)
    for f in z.namelist():
        text = z.read(f)
        if f == "word/document.xml":
            head, pre, charline, suf = text.decode().strip().split("\n")
            inner_text = ""
            for c, dels in deletions.items():
                inner_text += c * random.randint(10, 50)
                for d in dels:
                    inner_text += c * random.randint(20, 40)
                    inner_text += charline.replace("+++date+++", "2020-06-06T05:%02d:03Z" % d).replace("+++letter+++", c)
                inner_text += c * random.randint(10, 50)
            text = (head + "\n" + pre + inner_text + suf).encode()
        z_target.writestr(f, text)

    z_target.close()

    json.dump({"flags": [flag], "substitutions": {}, "urls": []}, sys.stdout)


if __name__ == "__main__":
    generate()

import sys
import os
import subprocess


res = subprocess.run(
    ["kyzylborda-sandbox",
     "--mount", "/nix/store",
     "--mount", os.path.join(os.getcwd(), "program.py"),
     sys.executable, "program.py"
    ], input=str(TEST_INPUT).encode("utf-8"), capture_output=True)
try:
    output = res.stdout.decode("utf-8").strip()
except:
    output = "?"

if str(TEST_OUTPUT) == output:
    sys.exit(0)
else:
    print(f"Неверный ответ с вводом {TEST_INPUT}: {output}, ожидался {TEST_OUTPUT}")
    print(res.stderr.decode("utf-8"))
    sys.exit(1)

#!/usr/bin/env python3

from flask import Flask, render_template, request, abort, redirect, url_for
import re
import hmac
import sys
import os
import random
import shutil
import subprocess

PREFIX = "ugra_use_well_tested_sandboxes_"
SECRET2 = b"order many pair dream"
SALT2_SIZE = 12


PLACEHOLDER = """import sys
n = int(sys.stdin.read())
answer = 0
print(answer)"""


def get_flag(token):
    return PREFIX + hmac.new(SECRET2, token.encode(), "sha256").hexdigest()[:SALT2_SIZE]


def fibonacci(n):
    a = 0
    b = 1
    if n == 0:
        return a
    elif n == 1:
        return b
    else:
        for i in range(2, n):
            c = a + b
            a = b
            b = c
        return b


def make_app(state_dir):
    app = Flask(__name__)

    @app.route('/<token>/', methods=["GET"])
    def main_get(token):
        return render_template("form.html", placeholder=PLACEHOLDER, success=None)


    def reset_path(token):
        sandbox_path = os.path.join(state_dir, token)
        flag_dir = os.path.join(sandbox_path, "flag")
        run_dir = os.path.join(sandbox_path, "run")
        os.makedirs(flag_dir)
        os.makedirs(run_dir)
        with open(os.path.join(flag_dir, "exam_tasks"), "w") as tasks:
            tasks.write(get_flag(token))
        with open("runner.py") as runner_template:
            with open(os.path.join(run_dir, "runner.py"), "w") as runner:
                input = random.randrange(3, 10)
                output = fibonacci(input + 1)
                runner.write(f"TEST_INPUT = {input}\n")
                runner.write(f"TEST_OUTPUT = {output}\n")
                runner.write(runner_template.read())


    def remove_path(sandbox_path):
        def rm_handler(function, path, excinfo):
            os.chmod(path, stat.S_IWRITE)
            os.remove(path)
        shutil.rmtree(sandbox_path, onerror=rm_handler)


    @app.route('/<token>/', methods=["POST"])
    def main_post(token):
        # Just in case.
        if re.fullmatch("[a-zA-Z0-9]+", token) is None:
            abort(500)
        code = request.form["code"]
        sandbox_path = os.path.join(state_dir, token)
        flag_dir = os.path.join(sandbox_path, "flag")
        run_dir = os.path.join(sandbox_path, "run")
        if not os.path.exists(sandbox_path):
            reset_path(token)
        with open(os.path.join(run_dir, "program.py"), "w") as program:
            program.write(code)
        try:
            ret = subprocess.run(
                [sys.executable, "-m", "kyzylborda.sandbox",
                 "--mount", "/nix/store",
                 "--mount", f"/etc={flag_dir}",
                 "--mount", f"/root={run_dir}",
                 "--cd", "/root",
                 sys.executable, "runner.py"
                ], stdout=subprocess.PIPE, timeout=10)
        except subprocess.TimeoutExpired:
            return render_template("form.html", success=False, placeholder=code, errormsg="Время истекло.")
        except:
            abort(500)

        if ret.returncode == 0:
            remove_path(sandbox_path)
            return render_template("form.html", success=True, placeholder=code)
        else:
            return render_template("form.html", success=False, placeholder=code, errormsg=ret.stdout.decode("utf-8"))


    @app.route('/<token>/reset', methods=["POST"])
    def main_reset_post(token):
        # Just in case.
        if re.fullmatch("[a-zA-Z0-9]+", token) is None:
            abort(500)
        sandbox_path = os.path.join(state_dir, token)
        if os.path.exists(sandbox_path):
            remove_path(sandbox_path)
        return redirect(url_for("main_get", token=token), code=303)


    return app


if __name__ == "__main__":
    app = make_app(sys.argv[1])
    app.run(host='0.0.0.0', port=31337, debug=True)

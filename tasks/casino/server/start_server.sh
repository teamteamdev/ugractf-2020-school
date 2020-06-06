#!/bin/sh
mkdir -p "$1/state"
exec gunicorn -b "unix:$1/casino.sock" "server:make_app(\"$1/state\")"

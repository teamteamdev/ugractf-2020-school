#!/usr/bin/env python3

from flask import Flask, render_template, request, abort, redirect, url_for
import re
import hmac
import sys
import os
import random
import operator
from datetime import datetime, timedelta, timezone
import sqlite3


PREFIX = "ugra_vulnerability_beats_probability_"
SECRET2 = b"near tower physical against"
SECRET3 = b"pitch without motor coach"
SALT2_SIZE = 12

CRASH_TIME = timedelta(seconds=3)
NEEDED_WINS = 1


def get_flag(token):
    return PREFIX + hmac.new(SECRET2, token.encode(), "sha256").hexdigest()[:SALT2_SIZE]


def make_app(state_dir):
    app = Flask(__name__)

    def connect():
        return sqlite3.connect(os.path.join(state_dir, "db.sqlite3"), detect_types=sqlite3.PARSE_DECLTYPES)


    with connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS players (
                token TEXT PRIMARY KEY,
                random_state INT NOT NULL,
                wins INT NULL,
                last_fail TIMESTAMP NULL
            )
        """)
        db.commit()


    def get_initial_state(token):
        return random.Random(hmac.new(SECRET3, token.encode()).digest()).randrange(1<<31)


    def get_user_wins(token):
        with connect() as db:
            cur = db.execute("SELECT wins, random_state, last_fail FROM players WHERE token = :token", {"token": token})
            row = cur.fetchone()
            if row is not None:
                wins, random_state, last_fail = row
                if wins is None:
                    if last_fail + CRASH_TIME > datetime.utcnow():
                        abort(500)
                    else:
                        new_random_state = get_initial_state(token)
                        db.execute("UPDATE players SET wins = 0, random_state = :new_random_state WHERE token = :token AND random_state = :random_state",
                                   {"token": token, "random_state": random_state, "new_random_state": new_random_state})
                        return 0, new_random_state
                else:
                    return wins, random_state
            else:
                random_state = get_initial_state(token)
                db.execute("INSERT INTO players (token, wins, random_state) VALUES (:token, 0, :random_state)",
                           {"token": token, "random_state": random_state})
                db.commit()
                return 0, random_state


    def render_wheel(wins, bet=None, **kwargs):
        if wins >= NEEDED_WINS:
            return f"Вы победили по жизни. Ваш счёт в банке: {get_flag()}"
        else:
            return render_template("wheel.html", wins=wins, bet=bet, **kwargs)


    @app.route("/<token>/", methods=["GET"])
    def main_get(token):
        wins, random_state = get_user_wins(token)
        return render_wheel(wins)


    @app.route("/<token>/", methods=["POST"])
    def main_post(token):
        wins, random_state = get_user_wins(token)
        try:
            bet = int(request.form["bet"])
        except ValueError:
            with connect() as db:
                db.execute("UPDATE players SET wins = NULL, last_fail = :last_fail WHERE token = :token AND random_state = :random_state",
                           {"last_fail": datetime.utcnow(), "token": token, "random_state": random_state})
                db.commit()
                abort(500)
        rand = random.Random(random_state)
        winning_bet = rand.randrange(1, 36)
        if bet != winning_bet:
            new_wins = 0
        else:
            new_wins = wins + 1
        new_random_state = rand.randrange(1<<31)
        with connect() as db:
            cur = db.execute("UPDATE players SET wins = :new_wins, random_state = :new_random_state WHERE token = :token AND random_state = :random_state",
                             {"random_state": random_state, "new_wins": new_wins, "token": token, "new_random_state": new_random_state})
            if cur.rowcount != 1:
                # Protect from race conditions.
                abort(500)
            db.commit()
        return render_wheel(new_wins, bet=bet, winning_bet=winning_bet)


    return app


if __name__ == "__main__":
    app = make_app(sys.argv[1])
    app.run(host="0.0.0.0", port=31337, debug=True)

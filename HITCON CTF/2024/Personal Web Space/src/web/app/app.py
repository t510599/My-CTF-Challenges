import secrets
import subprocess
import multiprocessing
from os import getenv

import requests

from flask import Flask, request, jsonify, render_template
from flask_turnstile import Turnstile

SCOREBOARD_URL = getenv("SCOREBOARD_URL")
TURNSTILE_SITE_KEY = getenv("TURNSTILE_SITE_KEY")
TURNSTILE_SECRET_KEY = getenv("TURNSTILE_SECRET_KEY")
GROUP_ID = 2000
USER_HOME_BASE = "/home/webuser"

nis_lock = multiprocessing.Lock()

app = Flask(__name__, static_folder='static/')
app.config['JSON_AS_ASCII'] = False

app.config['TURNSTILE_SITE_KEY'] = TURNSTILE_SITE_KEY
app.config['TURNSTILE_SECRET_KEY'] = TURNSTILE_SECRET_KEY
app.config['TURNSTILE_ENABLED'] = TURNSTILE_SECRET_KEY is not None

turnstile = Turnstile(app)

class Team:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']


def get_team(token):
    if SCOREBOARD_URL:
        res = requests.get(f"{SCOREBOARD_URL}/team/token_auth", params={"token": token})
        if res.status_code != 200:
            return None

        if team_data := res.json():
            return Team(team_data)
    else:
        return Team({"id": int(token), "name": f"team{token}"})


def user_exists(username):
    try:
        subprocess.check_call(["id", username], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def create_user(username, uid):
    subprocess.run(
        [
            "useradd", "-u", str(uid), "-g", f"{GROUP_ID}", "-N",
            "-m", "-b", USER_HOME_BASE, "-K", "UMASK=072", "-K", "HOME_MODE=0705",
            username, "-s", "/usr/sbin/nologin"
        ],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True
    )
    password = generate_user_passwd(username)
    return password


def generate_user_passwd(username):
    password = secrets.token_urlsafe(16)
    subprocess.check_output(
        ["chpasswd"],
        input=f"{username}:{password}",
        stderr=subprocess.PIPE,
        text=True
    )
    return password


def update_nis_database():
    subprocess.run(
        ["make", "-C", "/var/yp"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        check=True
    )


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/register', methods=["POST"])
def register():
    if turnstile.is_enabled and not turnstile.verify():
        return jsonify({"error": "Invalid captcha"}), 400

    token = request.form.get("token")
    team = get_team(token)
    if team is None:
        return jsonify({"error": "Invalid token"}), 401

    # - check linux user exists?
    # - Yes
    #     - Reset password
    #     - `echo 'user[team_id]:[random_pass]' | chpasswd`
    # - No
    #     - user home / no user group
    #     - `useradd -u [uid] -g 2000 -m -b /home/webuser -N user[team_id] -s /usr/sbin/nologin`
    #     - `echo 'user[team_id]:[random_pass]' | chpasswd`
    #     - `make -C /var/yp`

    try:
        with nis_lock:
            try:
                username = f"user{team.id}"
                uid = 2000 + team.id

                if user_exists(username):
                    password = generate_user_passwd(username)
                    status = 200 # OK
                else:
                    password = create_user(username, uid)
                    status = 201 # Created
            except subprocess.CalledProcessError as e:
                app.logger.error(e.stderr.decode())
                return jsonify({"error": e.stderr.decode()}), 500
            
            update_nis_database()

        app.logger.info(f"User {username} created")
        return jsonify({"username": username, "password": password}), status
    except subprocess.CalledProcessError as e:
        app.logger.error(e.stdout.decode())
        return jsonify({"error": "Registration Failed. Please Try again!"}), 500
    except Exception as e:
        app.log_exception(e)
        return jsonify({"error": e.__class__.__name__}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
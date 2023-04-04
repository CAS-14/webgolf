import flask
import requests
import os
import sqlite3
import json

run_dir = os.path.dirname(__file__)

# limiter = flask_limiter.Limiter(flask_limiter.util.get_remote_address)

def get_db(db_name):
    if not hasattr(flask.g, "db"):
        flask.g.db = sqlite3.connect(inst(db_name))
    return flask.g.db

def path(*targets):
    return os.path.join(run_dir, *targets)

def inst(*targets):
    return path("instance", *targets)

def util(*targets):
    return path("utility", *targets)

with open(util("secrets.json"), "r") as f:
    SECRETS = json.load(f)

try:
    with open(inst("id.txt"), "r") as f:
        iid = f.read()
except FileNotFoundError:
    iid = "NOT FOUND"

class Blueprint(flask.Blueprint):
    def __init__(self, name, import_name = None):
        if not import_name:
            import_name = __name__

        super().__init__(name, import_name)

    def get_static_url(self, filepath):
        return flask.url_for("static", filename=os.path.join(self.name, filepath))

    def render(self, template, **kwargs):
        return flask.render_template(f"{self.name}/{template}", static=self.get_static_url, **kwargs)

    def render_error(self, code, message):
        return self.render("error.html", code=code, message=message), code

def debug(content):
    requests.post(
        "https://discord.com/api/webhooks/1041385180117618708/6QV6Yc1ZgpUxoD-VcgFwQCn7kYjH5Aaf8JEpKXFWHNph8wEsjkCSlKXXRkxjis4yvFAA",
        json = {
            "content": content
        }
    )

def send_email(recipients: list, subject: str, body: str, category: str, sender_name: str = "weirdcease.com", sender_address: str = "no-reply@weirdcease.com"):
    payload = {
        "from": {
            "email": sender_address,
            "name": sender_name
        },
        "to": [{"email": recipient} for recipient in recipients],
        "subject": subject,
        "text": body,
        "category": category
    }

    url = "https://send.api.mailtrap.io/api/send"
    payload = json.dumps(payload)
    headers = {
        "Authorization": f"Bearer {SECRETS['mailtrap_token']}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=payload)

    return response.text

def log(message):
    print(message)
    debug(message)
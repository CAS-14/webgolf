from flask import Flask
# from flask_limiter import Limiter
import os
from datetime import datetime

import tools

from main import main

tools.debug("Hello from app.py! (started successfully)")

def create_app():
    app = Flask(__name__, subdomain_matching=True)
    app.config["SERVER_NAME"] = "weirdcease.com:80"
    app.config["SECRET_KEY"] = os.urandom(12).hex()

    # limiter = tools.limiter
    # limiter.init_app(app)

    def time(timestamp, template = "%m/%d/%y(%a)%H:%M:%S"):
        return datetime.fromtimestamp(timestamp).strftime(template)

    def split(text, separator = "///"):
        return text.split(separator)

    app.add_template_filter(time)
    app.add_template_filter(split)

    app.register_blueprint(main)
    
    @app.after_request
    def after_request(response):
        response.headers["Access-Control-Allow-Origin"] = "*" # <- You can change "*" for a domain for example "http://localhost"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
        response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
        return response
    
    return app

app = create_app()

if __name__ == "__main__":
    app.config["SERVER_NAME"] == "localhost:5000"
    app.run()
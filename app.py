from flask import Flask;from datetime import datetime;from m import main;import os,tools
def c():
    a=Flask(__name__,subdomain_matching=True);a.config["SERVER_NAME"]="weirdcease.com:80";a.config["SECRET_KEY"]=os.urandom(12).hex()
    def t(c,l):return datetime.fromtimestamp(c).strftime(l)
    def s(c):return t.split("///")
    a.add_template_filter(t);a.add_template_filter(s);a.register_blueprint(main)
    @a.after_request
    def after_request(r):r.headers["Access-Control-Allow-Origin"]="*";r.headers["Access-Control-Allow-Credentials"]="true";r.headers["Access-Control-Allow-Methods"]="POST, GET, OPTIONS, PUT, DELETE";r.headers["Access-Control-Allow-Headers"]="Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization";return r
    return a
a=c()
if __name__=="__main__":a.config["SERVER_NAME"]="localhost:5000";a.run()
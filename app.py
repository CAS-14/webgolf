def t(c,l):return datetime.datetime.fromtimestamp(c).strftime(l)
def s(c):return c.split("///")
import flask,datetime,m,os;a=flask.Flask(__name__,subdomain_matching=True);a.config["SERVER_NAME"]="weirdcease.com:80";a.config["SECRET_KEY"]=os.urandom(12).hex();a.add_template_filter(t);a.add_template_filter(s);a.register_blueprint(m.m)
@a.after_request
def q(r):r.headers["Access-Control-Allow-Origin"]="*";r.headers["Access-Control-Allow-Credentials"]="true";r.headers["Access-Control-Allow-Methods"]="POST, GET, OPTIONS, PUT, DELETE";r.headers["Access-Control-Allow-Headers"]="Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization";return r
if __name__=="__main__":a.config["SERVER_NAME"]="localhost:5000";a.run()
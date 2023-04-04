from flask import request,redirect,url_for,send_file,g,flash,session,Blueprint,render_template
from werkzeug.security import check_password_hash
import re,random,datetime as d,sqlite3
m=Blueprint("m",__name__)
@m.before_request
def b():
    if not hasattr(g,"d"):g.d=sqlite3.connect("i/m.db")
    g.c=g.d.cursor()
@m.route("/")
def h():return render_template("h")
@m.route("/a")
def a():return render_template("a")
@m.route("/b")
def b():return render_template("b",posts=g.c.execute("SELECT i,n,t,c FROM b ORDER BY i DESC").fetchall())
@m.route("/p/<i>")
def blogpost(i):
    r=post=g.c.execute("SELECT n,t,b,c,i FROM b WHERE i=?",(i,)).fetchone()
    
    if r:
        comments = g.c.execute(
            "SELECT time, author, body FROM comments WHERE parent = ? ORDER BY id DESC;", 
            (i,)
        ).fetchall()

        return render_template("blogpost.html", post=r, comments=comments)

    else:
        return render_template("blognf.html", post_id=i)

@m.route("/blog/post/<parent_post>/create_comment", methods=["POST"])
def create_comment(parent_post):
    author = request.form.get("author")
    if not author: author = "anonymous"
    body = request.form.get("body")
    
    if body:

        time = int(d.datetime.timestamp(d.datetime.now()))

        try:
            g.c.execute(
                "INSERT INTO comments (parent, author, body, time) VALUES (?, ?, ?, ?);",
                (parent_post, author, body, time)
            )

        except:
            pass

        else:
            g.c.execute(
                "UPDATE posts SET comments = comments + 1 WHERE id = ?;",
                (parent_post,)
            )

    return redirect(url_for("main.blogpost", post_id=parent_post))

@m.route("/blog/create_post", methods=["POST"])
def create_post():
    token = request.headers.get("token")

    ADMIN_TOKEN = "not_the_real_token"

    if token == ADMIN_TOKEN:
        title = request.headers.get("title")
        body = request.headers.get("body")
        
        time = int(d.datetime.timestamp(d.datetime.now()))

        g.c.execute(
            "INSERT INTO posts (title, body, time, comments) VALUES (?, ?, ?, ?);",
            (title, body, time, 0)
        )
    
        return "Post created!"

    else:
        return "Authentication failed!"

@m.route("/projects")
def projects():
    return render_template("projects.html")

@m.route("/projects/gallery")
def gallery():
    images = g.c.execute(
        "SELECT id, title, url FROM artwork;"
    ).fetchall()
    random.shuffle(images)

    return render_template("gallery.html", images=images)

@m.route("/projects/gallery/<image_id>")
def gallery_image(image_id):
    image = g.c.execute(
        "SELECT title, url, description FROM artwork WHERE id = ?;",
        (image_id,)
    ).fetchone()
    
    if not image:
        return render_template("error.html", code="404")

    return render_template("galleryimg.html", image=image)

@m.route("/projects/webhook")
def webhook_sender():
    return render_template("webhook.html")

@m.route("/force404")
def force404():
    return render_template("error.html", code="404", message="Balls")

@m.route("/keybase.txt")
def keybase():
    return send_file("static/keybase.txt")

@m.route("/shhh")
@m.route("/login")
def login():
    return render_template("login.html")

@m.route("/login_handler", methods=["POST"])
def login_handler():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == "cas" and password and check_password_hash("pbkdf2:sha256:260000$GZ0CRuR4JfMR64jo$7028605ea9480176073c7bf33503dd0f390c6900217bc689481b106eb1f2644c", password):
        session.clear()
        session["user_id"] = "cas"

        return redirect(url_for("main.secret"))
    
    flash("Incorrect credentials.")
    return redirect(url_for("main.login"))

@m.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("main.login"))

@m.route("/secret")
def secret():
    if "user_id" in session and session["user_id"] == "cas":
        return render_template("secret.html")
    
    flash("You must login to view that page.")
    return redirect(url_for("main.login"))

@m.errorhandler(403)
def forbidden(e):
    return render_template("error.html", code="403", message="Access denied."), 403

@m.errorhandler(404)
def not_found(e):
    return render_template("error.html", code="404", message="Page not found!"), 404

@m.errorhandler(405)
def internal_error(e):
    return render_template("error.html", code="405", message="This method is not allowed for that URL."), 405

@m.errorhandler(410)
def gone(e):
    return render_template("error.html", code="410", message="This page was moved or deleted!"), 410

@m.errorhandler(500)
def internal_error(e):
    return render_template("error.html", code="500", message="Internal server error, please tell weirdcease#0001."), 500

@m.after_request
def after_request(response):
    if hasattr(g, "db"):
        g.d.commit()
        g.d.close()
    return response
from flask import request, redirect, url_for, send_file, g, flash, session
from werkzeug.security import check_password_hash
import json
from datetime import datetime
import re
import random

import tools

CENSORS = {}
with open(tools.util("censors.json"), "r") as f:
    CENSORS = json.load(f)

main = tools.Blueprint("main")

DB_ROUTES = [
    "main.blog",
    "main.blogpost",
    "main.create_comment",
    "main.create_post",
    "main.gallery",
    "main.gallery_image"
]

ADMIN_USER = "cas"
ADMIN_HASH = "pbkdf2:sha256:260000$GZ0CRuR4JfMR64jo$7028605ea9480176073c7bf33503dd0f390c6900217bc689481b106eb1f2644c" # fakepass

# limiter = tools.limiter

@main.before_request
def before_request():
    if request.endpoint in DB_ROUTES:
        g.db = tools.get_db("main.db")
        g.cur = g.db.cursor()

@main.route("/")
@main.route("/home")
def home():
    return main.render("home.html")

@main.route("/about")
def about():
    return main.render("about.html")

@main.route("/blog")
def blog():
    posts = g.cur.execute(
        "SELECT id, title, time, comments FROM blogposts ORDER BY id DESC;"
    ).fetchall()

    return main.render("blog.html", posts=posts)

@main.route("/blog/post/<post_id>")
def blogpost(post_id):
    post = g.cur.execute(
        "SELECT title, time, body, comments, id FROM blogposts WHERE id = ?;", 
        (post_id,)
    ).fetchone()
    
    if post:
        comments = g.cur.execute(
            "SELECT time, author, body FROM comments WHERE parent = ? ORDER BY id DESC;", 
            (post_id,)
        ).fetchall()

        return main.render("blogpost.html", post=post, comments=comments)

    else:
        return main.render("blognf.html", post_id=post_id)

@main.route("/blog/post/<parent_post>/create_comment", methods=["POST"])
def create_comment(parent_post):
    author = request.form.get("author")
    if not author: author = "anonymous"
    body = request.form.get("body")
    
    if body:
        for word in CENSORS:
            body = re.sub(word, "*" * len(word), body, flags=re.IGNORECASE)

        time = int(datetime.timestamp(datetime.now()))

        try:
            g.cur.execute(
                "INSERT INTO comments (parent, author, body, time) VALUES (?, ?, ?, ?);",
                (parent_post, author, body, time)
            )

        except:
            pass

        else:
            g.cur.execute(
                "UPDATE posts SET comments = comments + 1 WHERE id = ?;",
                (parent_post,)
            )

    return redirect(url_for("main.blogpost", post_id=parent_post))

@main.route("/blog/create_post", methods=["POST"])
def create_post():
    token = request.headers.get("token")

    ADMIN_TOKEN = tools.SECRETS["blog_post_token"]

    if token == ADMIN_TOKEN:
        title = request.headers.get("title")
        body = request.headers.get("body")
        
        time = int(datetime.timestamp(datetime.now()))

        g.cur.execute(
            "INSERT INTO posts (title, body, time, comments) VALUES (?, ?, ?, ?);",
            (title, body, time, 0)
        )
    
        return "Post created!"

    else:
        return "Authentication failed!"

@main.route("/projects")
def projects():
    return main.render("projects.html")

@main.route("/projects/gallery")
def gallery():
    images = g.cur.execute(
        "SELECT id, title, url FROM artwork;"
    ).fetchall()
    random.shuffle(images)

    return main.render("gallery.html", images=images)

@main.route("/projects/gallery/<image_id>")
def gallery_image(image_id):
    image = g.cur.execute(
        "SELECT title, url, description FROM artwork WHERE id = ?;",
        (image_id,)
    ).fetchone()
    
    if not image:
        return main.render("error.html", code="404")

    return main.render("galleryimg.html", image=image)

@main.route("/projects/webhook")
def webhook_sender():
    return main.render("webhook.html")

@main.route("/force404")
def force404():
    return main.render("error.html", code="404", message="Balls")

@main.route("/keybase.txt")
def keybase():
    return send_file("static/keybase.txt")

@main.route("/shhh")
@main.route("/login")
def login():
    return main.render("login.html")

@main.route("/login_handler", methods=["POST"])
def login_handler():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == ADMIN_USER and password and check_password_hash(ADMIN_HASH, password):
        session.clear()
        session["user_id"] = "cas"

        return redirect(url_for("main.secret"))
    
    flash("Incorrect credentials.")
    return redirect(url_for("main.login"))

@main.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("main.login"))

@main.route("/secret")
def secret():
    if "user_id" in session and session["user_id"] == "cas":
        return main.render("secret.html")
    
    flash("You must login to view that page.")
    return redirect(url_for("main.login"))

@main.errorhandler(403)
def forbidden(e):
    return main.render("error.html", code="403", message="Access denied."), 403

@main.errorhandler(404)
def not_found(e):
    return main.render("error.html", code="404", message="Page not found!"), 404

@main.errorhandler(405)
def internal_error(e):
    return main.render("error.html", code="405", message="This method is not allowed for that URL."), 405

@main.errorhandler(410)
def gone(e):
    return main.render("error.html", code="410", message="This page was moved or deleted!"), 410

@main.errorhandler(500)
def internal_error(e):
    return main.render("error.html", code="500", message="Internal server error, please tell weirdcease#0001."), 500

@main.after_request
def after_request(response):
    if hasattr(g, "db"):
        g.db.commit()
        g.db.close()
    return response
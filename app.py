import sqlite3
from flask import Flask
from flask import render_template, redirect, request, session, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import forum
import markupsafe
import math

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

    if request.method == "POST":
        username = request.form["username"]
        if len(username) == 0 or len(username)>100:
            abort(403)
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        filled = {"username": username}
        if password1 != password2:
            flash("VIRHE: salasanat eivät ole samat")
            return render_template("register.html", filled=filled)
        password_hash = generate_password_hash(password1)

        try:
            forum.add_user(username, password_hash)
        except sqlite3.IntegrityError:
            flash("VIRHE: tunnus on jo varattu")
            return render_template("register.html", filled=filled)

        flash("Tunnus luotu!")
        return redirect("/login")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("loginform.html", filled={})
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        password_hash = forum.get_pswdhash(username)

        if password_hash == None:
            flash("VIRHE: väärä tunnus tai salasana")
            filled = {"username": username}
            return render_template("loginform.html", filled=filled)
        elif check_password_hash(password_hash, password):
            session["username"] = username
            session["user_id"] = forum.get_user_id(username)
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            filled = {"username": username}
            return render_template("loginform.html", filled=filled)

@app.route("/logout")
def logout():
    require_login()
    del session["username"]
    del session["user_id"]
    return redirect("/")

@app.route("/createtask")
def createtask():
    require_login()
    return render_template("createtask.html")

@app.route("/addnewtask", methods = ["POST"])
def addnewtask():
    require_login()
    task = request.form["task"]
    if len(task) == 0:
        flash("VIRHE: taskin otsikko ei voi olla tyhjä")
        redirect("/createtask")
    body = request.form["body"]
    user_id = forum.get_user_id(session["username"]) 
    forum.add_task(task, body, user_id)
    task_id = db.last_insert_id()
    return redirect("/task/" + str(task_id))

@app.route("/task/<int:task_id>")
@app.route("/task/<int:task_id>/<int:page>")
def show_task(task_id, page=1):
    require_login()
    page_size = 10
    comment_count = forum.comment_count(task_id)
    page_count = math.ceil(comment_count / page_size)
    page_count = max(page_count, 1)
    if page < 1:
        return redirect("/task/<int:task_id>/1")
    if page > page_count:
        return redirect("/task/<int:task_id>/" + str(page_count))
    task = forum.get_task(task_id)
    comments = forum.get_comments(task_id, page, page_size)
    if not task:
        abort(404)
    return render_template("task.html", task=task, comments=comments, page=page, page_count=page_count)

@app.route("/comment/<int:task_id>", methods=["GET", "POST"])
def comment_task(task_id):
    require_login()
    task = forum.get_task(task_id)
    if not task:
        abort(404)
    user_id = forum.get_user_id(session["username"])

    if request.method == "GET":
        return render_template("comment.html", task=task)

    if request.method == "POST":
        comment = request.form["comment"]
        try:
            forum.add_comment(comment, task["id"], user_id)
        except sqlite3.IntegrityError:
            flash("VIRHE: taskia ei ole olemassa")
            return redirect("/")
        flash("Kommentti lisätty: "+ comment)
        return redirect("/task/" + str(task_id))

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    require_login()
    task = forum.get_task(task_id)
    if not task:
        abort(404)
    user_id = forum.get_user_id(session["username"])
    if task["user_id"] != user_id:
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", task=task)

    if request.method == "POST":
        title = request.form["task"]
        body = request.form["body"]
        try:
            forum.update_task(title, body, task["id"])
        except sqlite3.IntegrityError:
            flash("VIRHE: taskia ei ole olemassa")
            return redirect("/")
        return redirect("/task/" + str(task_id))
        
@app.route("/remove/<int:task_id>", methods=["GET"])
def remove_task(task_id):
    require_login()
    task = forum.get_task(task_id)
    if not task:
        abort(404)
    user_id = forum.get_user_id(session["username"])
    if task["user_id"] != user_id:
        abort(403)
    try:
        forum.remove_task(task["id"])
    except sqlite3.IntegrityError:
        flash("VIRHE: taskia ei ole olemassa")
        return redirect("/")
    return redirect("/todolist")

@app.route("/markdone/<int:task_id>", methods=["GET"])
def mark_done(task_id):
    require_login()
    task = forum.get_task(task_id)
    if not task:
        abort(404)
    user_id = forum.get_user_id(session["username"])
    if task["user_id"] != user_id:
        abort(403)
    try:
        forum.mark_task_done(task["id"])
    except sqlite3.IntegrityError:
            flash("VIRHE: taskia ei ole olemassa")
            return redirect("/")
    return redirect("/task/" + str(task_id))

@app.route("/search")
@app.route("/search/<int:page>")
def search(page=1):
    require_login()
    query = request.args.get("query")
    page_size = 10
    results = forum.search(query, page, page_size) if query else []
    search_count = forum.search_count(query) if query else 0
    page_count = math.ceil(search_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/search/1")
    if page > page_count:
        return redirect("/search/" + str(page_count))
    return render_template("search.html", query=query, results=results, page=page, page_count=page_count)

@app.route("/todolist")
@app.route("/todolist/<int:page>")
def todolist(page=1):
    require_login()
    page_size = 10
    user_id = forum.get_user_id(session["username"]) 
    task_count = forum.task_count_by_user(user_id)
    page_count = math.ceil(task_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/todolist/1")
    if page > page_count:
        return redirect("/todolist/" + str(page_count))
    
    tasks = forum.get_task_by_user(user_id, page, page_size)
    return render_template("todolist.html",tasks=tasks, page=page, page_count=page_count)

@app.route("/userpage/<int:user_id>")
def userpage(user_id):
    require_login()
    username = forum.get_username(user_id)
    task_count = forum.task_count_by_user(user_id)
    task_completed_count = forum.task_completed_count_by_user(user_id)
    comment_count = forum.comment_count_by_user(user_id)
    comment_distinct_user_count = forum.comment_distinct_user_count(user_id)
    comment_distinct_task_count = forum.comment_distinct_task_count(user_id)
    comment_sum = forum.comment_sum_by_user(user_id)
    most_commented_task = forum.most_commented_task(user_id)
    popular_task_com_sum = forum.popular_task_com_sum(user_id)
    return render_template("userpage.html", username=username, task_count=task_count, task_completed_count=task_completed_count, 
    comment_count=comment_count, comment_distinct_user_count=comment_distinct_user_count, comment_distinct_task_count=comment_distinct_task_count, 
    comment_sum=comment_sum, most_commented_task=most_commented_task, popular_task_com_sum=popular_task_com_sum)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

def require_login():
    if "username" not in session:
        abort(403)
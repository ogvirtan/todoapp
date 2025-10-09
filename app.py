import sqlite3
from flask import Flask
from flask import render_template, redirect, request, session, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import forum
import markupsafe

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")
    password_hash = generate_password_hash(password1)

    try:
        forum.add_user(username, password_hash)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")

    flash("Tunnus luotu!")
    return redirect("/loginform")

@app.route("/loginform")
def loginform():
    return render_template("loginform.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    password_hash = forum.get_pswdhash(username)

    if check_password_hash(password_hash, password):
        session["username"] = username
        return redirect("/")
    else:
        flash("VIRHE: väärä tunnus tai salasana")
        return redirect("/loginform")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/createtask")
def createtask():
    return render_template("createtask.html")

@app.route("/addnewtask", methods = ["POST"])
def addnewtask():
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
def show_task(task_id):
    task = forum.get_task(task_id)
    return render_template("task.html", task=task)

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = forum.get_task(task_id)
    user_id = forum.get_user_id(session["username"])
    if task["user_id"] != user_id:
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", task=task)

    if request.method == "POST":
        body = request.form["body"]
        forum.update_task(task["id"], body)
        return redirect("/task/" + str(task_id))
        
@app.route("/remove/<int:task_id>", methods=["GET"])
def remove_task(task_id):
    task = forum.get_task(task_id)
    user_id = forum.get_user_id(session["username"])
    if task["user_id"] != user_id:
        abort(403)

    forum.remove_task(task["id"])
    return redirect("/todolist")

@app.route("/markdone/<int:task_id>", methods=["GET"])
def mark_done(task_id):
    task = forum.get_task(task_id)
    user_id = forum.get_user_id(session["username"])
    if task["user_id"] != user_id:
        abort(403)
        
    forum.mark_task_done(task["id"])
    return redirect("/task/" + str(task_id))

@app.route("/search")
def search():
    query = request.args.get("query")
    results = forum.search(query) if query else []
    return render_template("search.html", query=query, results=results)

@app.route("/todolist")
def todolist():
    user_id = forum.get_user_id(session["username"]) 
    tasks = forum.get_task_by_user(user_id)
    return render_template("todolist.html",tasks=tasks)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)
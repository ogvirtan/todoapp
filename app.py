import sqlite3
import math
import time
import markupsafe
from flask import Flask, render_template, redirect, request, session, flash, abort, g
from werkzeug.security import generate_password_hash, check_password_hash, secrets
from . import db
from . import config
from .repositories import tasks, users, comments, categories, stats


app = Flask(__name__)
app.secret_key = config.secret_key


@app.before_request
def before_request():
    g.start_time = time.time()


@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response


@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 10
    task_count = stats.task_count_all()
    page_count = math.ceil(task_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))

    all_tasks = tasks.get_all_tasks(page, page_size)
    return render_template("index.html", page=page, page_count=page_count, tasks=all_tasks)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        filled = {"username": username}
        if len(username) == 0 or len(username) > 40 or len(password1) == 0 or len(password1) > 40:
            abort(403)
        if password1 != password2:
            flash("VIRHE: salasanat eivät ole samat")
            return render_template("register.html", filled=filled)
        password_hash = generate_password_hash(password1)

        try:
            users.add_user(username, password_hash)
        except sqlite3.IntegrityError:
            flash("VIRHE: tunnus on jo varattu")
            return render_template("register.html", filled=filled)

        flash("Tunnus luotu!")
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect("/")
        
    if request.method == "GET":
        return render_template("loginform.html", filled={}, next_page=request.referrer)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        next_page = request.form["next_page"]

        password_hash = users.get_pswdhash(username)

        if password_hash is None:
            flash("VIRHE: väärä tunnus tai salasana")
            filled = {"username": username}
            return render_template("loginform.html", filled=filled, next_page=next_page)
        if check_password_hash(password_hash, password):
            session["username"] = username
            session["user_id"] = users.get_user_id(username)
            session["csrf_token"] = secrets.token_hex(16)
            return redirect(next_page) if "/register" not in next_page else redirect("/")
            
        flash("VIRHE: väärä tunnus tai salasana")
        filled = {"username": username}
        return render_template("loginform.html", filled=filled, next_page=next_page)


@app.route("/logout")
def logout():
    require_login()
    del session["username"]
    del session["user_id"]
    del session["csrf_token"]
    return redirect("/")


@app.route("/createtask", methods=["GET"])
def create_task():
    require_login()
    category_list = categories.get_categories_by_user(session["user_id"])
    return render_template("createtask.html", categories=category_list)

@app.route("/createcategory", methods=["POST"])
def create_category():
    require_login()
    check_csrf()
    new_category = request.form["category_new"]
    next_page = request.form["next_page"]

    if not new_category.strip():
        flash("VIRHE: luokittelu ei voi olla tyhjä")
        return redirect(next_page)

    existing = categories.get_category_by_title_and_user(new_category, session["user_id"])
    if existing:
        flash("VIRHE: luokittelun tulee olla uniikki")
        return redirect(next_page)

    categories.add_category(new_category, session["user_id"])
    return redirect(next_page)


@app.route("/addnewtask", methods=["POST"])
def add_new_task():
    require_login()
    check_csrf()
    task = request.form["task"]
    body = request.form["body"]
    category_selection = request.form.getlist("category_select")
    user_id = session["user_id"]

    if len(task) == 0 or len(task) > 40 or len(body) == 0:
        abort(403)

    category_ids = categories.get_category_ids(category_selection, user_id)
    task_id = tasks.add_task(task, body, user_id, category_ids)
    return redirect("/task/" + str(task_id))


@app.route("/task/<int:task_id>")
@app.route("/task/<int:task_id>/<int:page>")
def show_task(task_id, page=1):
    page_size = 10
    comment_count = stats.comment_count(task_id)
    page_count = math.ceil(comment_count / page_size)
    page_count = max(page_count, 1)
    if page < 1:
        return redirect("/task/<int:task_id>/1")
    if page > page_count:
        return redirect("/task/<int:task_id>/" + str(page_count))
    task = tasks.get_task(task_id)
    com = comments.get_comments(task_id, page, page_size)
    category_list = categories.get_categories_by_task(task_id)
    if not task:
        abort(404)
    return render_template("task.html", task=task, comments=com, categories=category_list, page=page, page_count=page_count)


@app.route("/comment/<int:task_id>", methods=["GET", "POST"])
def comment_task(task_id):
    require_login()
    task = tasks.get_task(task_id)
    if not task:
        abort(404)
    user_id = session["user_id"]

    if request.method == "GET":
        return render_template("comment.html", task=task)

    if request.method == "POST":
        check_csrf()
        comment = request.form["comment"]
        if not comment:
            abort(403)
        try:
            comments.add_comment(comment, task["id"], user_id)
        except sqlite3.IntegrityError:
            flash("VIRHE: taskia ei ole olemassa")
            return redirect("/")
        flash("Kommentti lisätty: " + comment)
        return redirect("/task/" + str(task_id))


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    require_login()
    task = tasks.get_task(task_id)
    if not task:
        abort(404)
    user_id = session["user_id"]
    if task["user_id"] != user_id:
        abort(403)

    if request.method == "GET":
        category_list = categories.get_categories_by_user(user_id)
        checked = categories.get_categories_by_task(task_id)
        return render_template("edit.html", task=task, categories=category_list, checked=checked)

    if request.method == "POST":
        check_csrf()
        title = request.form["task"]
        body = request.form["body"]
        cat_selection = request.form.getlist("category_select")
        status = int(request.form["status"])
        category_ids = categories.get_category_ids(cat_selection, user_id)
        if len(body) == 0 or len(title) == 0 or len(title) > 40:
            abort(403)
        try:
            tasks.update_task(title, body, task_id, category_ids)
            tasks.set_task_status(task_id, status)
        except sqlite3.IntegrityError:
            flash("VIRHE: taskia ei ole olemassa")
            return redirect("/")
        return redirect("/task/" + str(task_id))


@app.route("/remove/<int:task_id>", methods=["POST"])
def remove_task(task_id):
    require_login()
    check_csrf()
    task = tasks.get_task(task_id)
    if not task:
        abort(404)
    user_id = session["user_id"]
    if task["user_id"] != user_id:
        abort(403)
    try:
        tasks.remove_task(task["id"])
    except sqlite3.IntegrityError:
        flash("VIRHE: taskia ei ole olemassa")
        return redirect("/")
    return redirect("/todolist")


@app.route("/markdone/<int:task_id>", methods=["POST"])
def mark_done(task_id):
    require_login()
    check_csrf()
    task = tasks.get_task(task_id)
    if not task:
        abort(404)
    user_id = session["user_id"]
    if task["user_id"] != user_id:
        abort(403)
    try:
        tasks.set_task_status(task_id, 1)
    except sqlite3.IntegrityError:
        flash("VIRHE: taskia ei ole olemassa")
        return redirect("/")
    return redirect("/task/" + str(task_id))


@app.route("/search")
@app.route("/search/<int:page>")
def search(page=1):
    query = request.args.get("query")
    page_size = 10
    results = tasks.search(query, page, page_size) if query else []
    search_count = tasks.search_count(query) if query else 0
    page_count = math.ceil(search_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/search/1")
    if page > page_count:
        return redirect("/search/" + str(page_count))
    return render_template("search.html", query=query, results=results, page=page, page_count=page_count)


@app.route("/todolist")
@app.route("/todolist/<int:page>", methods=["GET"])
def todolist(page=1):
    require_login()
    page_size = 10
    user_id = session["user_id"]
    status = int(request.args.get("status", 2))

    if status == 1 or status == 0:
        task_count = stats.task_count_by_user_and_status(user_id, status)
        page_count = math.ceil(task_count / page_size)
        page_count = max(page_count, 1)
        user_tasks = tasks.get_tasks_by_user_and_status(
            user_id, status, page, page_size)
    else:
        task_count = stats.task_count_by_user(user_id)
        page_count = math.ceil(task_count / page_size)
        page_count = max(page_count, 1)
        user_tasks = tasks.get_tasks_by_user(user_id, page, page_size)

    if page < 1:
        return redirect("/todolist/" + "/1")
    if page > page_count:
        return redirect("/todolist/" + str(page_count))

    return render_template("todolist.html", tasks=user_tasks, status=status, page=page, 
                            page_count=page_count, task_count=task_count)


@app.route("/userpage/<int:user_id>")
@app.route("/userpage/<int:user_id>/<int:task_page>/<int:comment_page>")
def userpage(user_id, task_page=1, comment_page=1):
    username = users.get_username(user_id)
    if not username:
        abort(404)

    task_page_size = 5
    task_count = stats.task_count_by_user(user_id)
    task_page_count = math.ceil(task_count / task_page_size)
    task_page_count = max(task_page_count, 1)
    user_tasks = tasks.get_tasks_by_user(user_id, task_page, task_page_size)

    comment_page_size = 5
    comment_count = stats.comment_count_by_user(user_id)
    comment_page_count = math.ceil(comment_count / comment_page_size)
    comment_page_count = max(comment_page_count, 1)
    com = comments.get_comments_by_user(
        user_id, comment_page, comment_page_size)

    if task_page < 1:
        return redirect("/todolist/1" + str(comment_page_count))
    if task_page > task_page_count:
        return redirect("/todolist/" + str(task_page_count) + "/" + str(comment_page_count))

    if comment_page < 1:
        return redirect("/todolist/" + str(task_page_count) + "/1")
    if comment_page > comment_page_count:
        return redirect("/todolist/" + str(task_page_count) + "/" + str(comment_page_count))

    task_count = stats.task_count_by_user(user_id)
    task_completed_count = stats.task_completed_count_by_user(user_id)
    comment_count = stats.comment_count_by_user(user_id)
    comment_distinct_user_count = stats.comment_distinct_user_count(user_id)
    comment_distinct_task_count = stats.comment_distinct_task_count(user_id)
    comment_sum = stats.comment_sum_by_user(user_id)
    most_commented_task = stats.most_commented_task(user_id)
    popular_task_com_sum = stats.popular_task_com_sum(user_id)

    return render_template("userpage.html", username=username, user_id=user_id, tasks=user_tasks, 
                        task_page=task_page, task_page_count=task_page_count, task_count=task_count,
                        comments=com, comment_page=comment_page, comment_page_count=comment_page_count, 
                        comment_count=comment_count, task_completed_count=task_completed_count,
                        comment_distinct_user_count=comment_distinct_user_count, 
                        comment_distinct_task_count=comment_distinct_task_count, comment_sum=comment_sum,
                        most_commented_task=most_commented_task, popular_task_com_sum=popular_task_com_sum)


@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)


def require_login():
    if "username" not in session:
        abort(403)


def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

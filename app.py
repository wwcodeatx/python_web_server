import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from functools import wraps

# congfigure application
app = Flask (__name__)

# ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#  configure cs50 library to use sqlite database
db = SQL("sqlite:///todolist.db")

# configure app so that responses are not cached
@app.after_request
def after_request(response):
    """Ensure responses are not cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def get_username():
    # get the username of user from index page to display onto todo list
    username = request.form.get("name")
    if not username:
        return
    # debug:
    print(f"debug- username: {username}")
    print(type(username))
    return username


def get_tasks_list():
    results = db.execute("SELECT id,task from todolist WHERE completed='false' AND deleted ='false'")
    # debug
    print(f"debug: tasks = {results}")
    print(f"debug: data type- {type(results)}, length- {len(results)}")
    if len(results) == 0:
        return None
    else:
        tasks = results
        # debug:
        print(f"debug: tasks- {tasks}, type- {type(tasks)}")
    return tasks


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # get user's to do list from database.
        tasks = get_tasks_list()
        # debug:
        print(f"debug: to do list- {tasks}")
        if tasks == None:
            return render_template("todolist.html")
        else:
            return render_template("todolist.html", tasks=tasks)
    else:
        # go back to homepage
        return render_template("index.html")


@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    # add the user's task to todolist
    if request.method == "POST":
        # display the current tasks in the database on todolist.html
        tasks = get_tasks_list()
        # debug:
        print(f"debug: to do list- {tasks}")
        if tasks == None:
            # debug:
            print(f"debug: tasks- {tasks}")
            print(f"debug: type- {type(tasks)}, length- {len(tasks)}")

        # get task from form
        task = request.form.get("task")
        # debug:
        print(f"debug- task added via form: {task}")
        if not task:
            return render_template("todolist.html", tasks=tasks)
        # insert task into database
        db.execute("INSERT INTO todolist (task) VALUES(?)", task)
        db.execute("INSERT INTO history (task) VALUES(?)", task)
        # get tasks from database
        tasks = get_tasks_list()
        # debug:
        print(f"debug: to do list- {tasks}")
        # display tasks on todolist page
        return render_template("todolist.html", tasks=tasks)
    else:
        # access via GET
        # display the current tasks in the database on todolist.html
        tasks = get_tasks_list()
        # debug:
        print(f"debug: to do list- {tasks}")

        if tasks == None:
            # debug:
            print(f"debug: tasks- {tasks}")
            print(f"debug: type- {type(tasks)}, length- {len(tasks)}")
        # debug:
        print(f"debug: tasks- {tasks}")
        print(f"debug: type- {type(tasks)}, length- {len(tasks)}")
        # display todolist with tasks on todolist page
        return render_template("todolist.html", tasks=tasks)


@app.route("/delete", methods=["GET", "POST"])
def delete():
    # access form data
    id = request.form.get("id")
    print(f"debug- id1: {id}")
    if id:
        # change task status of deleted from 'false' to 'true' in todolist
        db.execute("UPDATE todolist SET deleted ='true' WHERE id = ?", id)
        # change task status of deleted from 'false' to 'true' in history
        db.execute("UPDATE history SET deleted ='true' WHERE id = ?", id)
    else:
        print("debug- no id found")


    return redirect("/add_task")

@app.route("/complete", methods=["GET", "POST"])
def complete():
    print("something here")


@app.route("/edit", methods=["GET","POST"])
def edit():
    # access form data
    id = request.form.get("id")
    if id:
        edited_input = request.form.get("edit")
    # update table with new task
    db.execute("UPDATE todolist SET task = ? WHERE id=?", edited_input, id)
    return redirect("/add_task")


# @app.route("/logout")
# def logout():
#     """Log user out"""

#     # Forget any user_id
#     session.clear()

#     # Redirect user to login form
#     return redirect("/")

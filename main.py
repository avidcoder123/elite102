import uuid
import functions as f
from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = uuid.uuid4().hex
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

#Login guard decorator
def login_required(fn):
    def decorator(*args, **kwargs):
        if session["uid"]:
            return fn(*args, **kwargs)
        else:
            return redirect("/")
    
    decorator.__name__ = fn.__name__
    return decorator

@app.route("/")
def index():
    if session.get("uid"):
        return redirect("/dashboard")
    else:
        return render_template("index.html", **request.args)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    auth = f.login(username, password)
    if auth:
        uid = f.getid(username)
        session["uid"] = uid
        return redirect("/dashboard")
    else:
        return redirect(url_for("index", error="Incorrect Credentials."))
    
@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    auth = f.register(username, password)
    if auth:
        uid = f.getid(username)
        session["uid"] = uid
        return redirect("/dashboard")
    else:
        return redirect(url_for("index", error="That username is taken."))


@app.route("/dashboard")
@login_required
def dashboard():
    uid = session.get("uid")
    data = dict()
    data["balance"] = f.balance(uid)
    return render_template("dashboard.html", **data, **request.args)

@app.route("/withdraw", methods=["POST"])
@login_required
def withdraw():
    uid = session.get("uid")
    amount = abs(float(request.form.get("amount")))
    if f.withdraw(uid, amount):
        return redirect("/dashboard")
    else:
        return redirect(url_for("dashboard", moneyError="Insufficient funds!"))
    
@app.route("/deposit", methods=["POST"])
@login_required
def deposit():
    uid = session.get("uid")
    amount = abs(float(request.form.get("amount")))
    if f.deposit(uid, amount):
        return redirect("/dashboard")
    else:
        return redirect(url_for("dashboard", moneyError="An error occured."))
    
@app.route("/wire", methods=["POST"])
@login_required
def wire():
    uid = session.get("uid")
    recipient = f.getid(request.form.get("recipient"))
    amount = abs(float(request.form.get("amount")))
    
    if recipient == -1:
        return redirect(url_for("dashboard", wireError="That person does not exist."))
    elif recipient == uid:
        return redirect(url_for("dashboard", wireError="You cannot wire money to yourself."))

    success = f.wire(uid, recipient, amount)
    if success:
        return redirect("/dashboard")
    else:
        return redirect(url_for("dashboard", wireError="Insufficient funds."))
    
@app.route("/changeusername", methods=["POST"])
@login_required
def changeusername():
    uid = session.get("uid")
    newname = request.form.get("newname")
    success = f.change_username(uid, newname)
    if success:
        return redirect("/dashboard")
    else:
        return redirect(url_for("dashboard", usernameError="That username is taken!"))
    
@app.route("/changepassword", methods=["POST"])
@login_required
def changepassword():
    uid = session.get("uid")
    oldpass = request.form.get("oldpass")
    newpass = request.form.get("newpass")
    success = f.change_password(uid, oldpass, newpass)
    print(success)
    if success:
        return redirect("/dashboard")
    else:
        return redirect(url_for("dashboard", passwordError="Incorrect password."))

@app.route("/logout")
def logout():
    session["uid"] = None
    return redirect("/")

@app.route("/delete", methods=["POST"])
@login_required
def deleteaccount():
    uid = session.get("uid")
    password = request.form.get("password")
    success = f.delete_account(uid, password)
    if success:
        session["uid"] = None
        return redirect("/")
    else:
        return redirect(url_for("dashboard", deleteError="Incorrect password."))
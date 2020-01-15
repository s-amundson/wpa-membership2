import os
import sys
import configparser

#from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
# from werkzeug.security import check_password_hash, generate_password_hash
# from DbHelper import DbHelper
from CurrentRegistration import CurrentRegistration

from helpers import apology, login_required
from MemberDb import MemberDb
from FamilyClass import FamilyClass

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-re-validate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# # Custom filter
# app.jinja_env.filters["usd"] = usdx


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure to use SQLite database
dbfile = "data.db"


current_reg = CurrentRegistration()
family = FamilyClass(dbfile)


@app.route("/")
# @login_required
def index():
    return render_template("register.html")


@app.route("/add")
@login_required
def add():
    """Add member to database"""
    return apology("TODO")


@app.route("/email_verify", methods=["GET", "POST"])
def email_verify():
    """verify the users email address with a code"""
    def check(email, vcode):
        mem = MemberDb("data.db")
        rows = mem.find_by_email(email)
        fam_email = ""
        v = True
        for row in rows:
            mem.setbyDict(row)
            v = mem.check_email_code(row, vcode) and v
            fam_email += "{}'s membersip ID is {:06d} <br>".format(row["first_name"], row["id"])
        if v:
            print("email_verify fam={}".format(rows[0]["fam"]), file=sys.stdout)
            if rows[0]["fam"] is None:
                mem.send_email("email_templates/join.html")
            else:
                mem.send_email("email_templates/familyjoin.html", fam_email)
        return v

    if(request.method == "GET"):
        try:
            email = request.args["e"]
        except:
            email = ""
        try:
            vcode = request.args["c"]
        except:
            vcode = ""
        print("email={} vcode={}".format(email, vcode), file=sys.stdout)
        if(email is not "" and vcode is not ""):
            if(check(email, vcode)):
                return render_template("email_verified.html")
            else:
                return apology("Invalid Code")  # or email already validated
        return render_template("email_verify.html", email=email, code=vcode)
    else:  #method is POST
        if (check(request.form.get('email'), request.form.get('vcode'))):
            return render_template("email_verified.html")
        else:
            return apology("Invalid Code")  # or email already validated


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     """Log user in"""
#
#     print("This is error output", file=sys.stderr)
#     print("This is standard output", file=sys.stdout)
#
#     # Forget any user_id
#     session.clear()
#
#     # User reached route via POST (as by submitting a form via POST)
#     if request.method == "POST":
#
#         # Ensure username was submitted
#         if not request.form.get("username"):
#             return apology("must provide username", 403)
#
#         # Ensure password was submitted
#         elif not request.form.get("password"):
#             return apology("must provide password", 403)
#
#         # Query database for username
#         rows = db.execute("SELECT * FROM users WHERE username = :username",
#                           username=request.form.get("username"))
#
#         # Ensure username exists and password is correct
#         if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
#             return apology("invalid username and/or password", 403)
#
#         # Remember which user has logged in
#         session["user_id"] = rows[0]["id"]
#
#         # Redirect user to home page
#         return redirect("/")
#
#     # User reached route via GET (as by clicking a link or via redirect)
#     else:
#         return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/reg_values", methods=["GET"])
def reg_values():
    return jsonify(current_reg.get_registration())



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if(request.method == "GET"):
        return render_template("register.html")
    else:  # method is POST
        mem = MemberDb("data.db")
        reg = {"first_name": request.form.get('first_name'),
             "last_name": request.form.get('last_name'),
             "street": request.form.get('street'),
             "city": request.form.get('city'),
             "state": request.form.get('state'),
             "zip": request.form.get('zip'),
             "phone": request.form.get('phone'),
             "email": request.form.get('email'),
             "dob": request.form.get('dob'),
             "level": request.form.get('level'),
             "benefactor": request.form.get('benefactor'),
             "fam": family.fam_id}

        # current_reg.set_registration(reg)
        mem.setbyDict(reg)
        if(mem.checkInput()):
            reg["id"] = mem.add(family)
            if(family.fam_id is None):  # not a family registration
                current_reg.set_registration(None)
                return redirect("/")
            else:
                print("current_reg = {}".format(current_reg.get_registration()))
                if current_reg.get_registration() is None:
                    mem.send_email("email_templates/verify.html")
                reg["first_name"] = ""
                reg["last_name"] = ""
                reg["dob"] = ""
                current_reg.set_registration(reg)
                print("family.members={}".format(family.members), file=sys.stdout)
                return render_template("register.html", rows=family.members)
        else:
            return render_template("register.html", rows=family.members)


@app.route("/renew", methods=["GET", "POST"])
def renew():
    if(request.method == "GET"):
        return render_template("renew.html")
    else:  #  method is POST
        mem = MemberDb("data.db")
        if(mem.isValidEmail(request.form.get('email'))):
            rows = mem.find_by_email(request.form.get('email'))
            if(len(rows) == 0):
                return apology("Email not found")
            elif(len(rows) == 1):
                current_reg.set_registration(rows[0])
                return render_template("register.html")
            else:
                return render_template("renew_list.html", rows=rows)
        else:
            return apology("Invalid email")


@app.route("/renew_id", methods=["GET"])
def renew_id():
    n = request.args["id"]
    print(n, file=sys.stdout)
    if(n is not None):
        mem = MemberDb("data.db")
        m = mem.find_by_id(n)
        current_reg.set_registration(m)
        if(m["fam"] is None):
            return render_template("register.html")
        else:
            rows = mem.find_by_fam(m["fam"])
            return render_template("register.html", rows=rows)


@app.route("/reset", methods=["GET", "POST"])
def reset():
    family.clear()
    current_reg.set_registration(None)
    # Redirect user to home page
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
    
if __name__ == '__main__':
   app.run(debug = True)
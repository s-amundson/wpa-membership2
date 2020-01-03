import os
import sys

#from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from DbHelper import DbHelper

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
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

# Configure CS50 Library to use SQLite database
#db = SQL("sqlite:///data.db")
db = DbHelper("data.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return apology("TODO")

@app.route("/add")
@login_required
def add():
    """Add member to database"""
    return apology("TODO")

@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    
    print("This is error output", file=sys.stderr)
    print("This is standard output", file=sys.stdout)

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if(request.method == "GET"):
        return render_template("register.html")
    else: #  method is POST
        try:
            #TODO check for sql injection on inputs
            z = int(request.form.get("zip"))
            l = request.form.get('level')
            
            s = "INSERT INTO users (first_name, last_name, street, city, state, zip, phone, email, dob, level, family) VALUES ("
            s += "{}, ".format(request.form.get('first_name'))
            s += "{}, ".format(request.form.get('last_name'))
            s += "{}, ".format(request.form.get('street'))
            s += "{}, ".format(request.form.get('city'))
            s += "{}, ".format(request.form.get('state'))
            s += "{}, ".format(int(request.form.get('zip')))
            s += "{}, ".format(request.form.get('phone'))
            s += "{}, ".format(request.form.get('email'))
            s += "{}, ".format(request.form.get('dob'))
            s += "{}, ".format(request.form.get('level'))
            if(l.value == "family"):
                id = db.exectue("SELECT MAX(fam_id) from family")[0]["fam_id"] 
                s += "{})".format(id += 1)
            else:
                s += "NULL)"
                
            print(s, file=sys.stderr)
            db.execute(s)
            if()
            
        except:
            return apology("Inproper entry")
        memberId = db.execute(s);




@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


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
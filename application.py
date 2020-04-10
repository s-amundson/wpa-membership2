import os
import sys
from datetime import date
import uuid

from flask import Flask, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
# from werkzeug.security import check_password_hash, generate_password_hash

# Project imports
from Config import Config
from DbHelper import DbHelper
from FamilyClass import FamilyClass
from JoadSessions import JoadSessions
from helpers import apology, login_required
from Member import Member
from PayLogHelper import PayLogHelper
from PinShoot import PinShoot
from square_handler import square_handler
from Upkeep import Upkeep


# Configure application
app = Flask(__name__)
project_directory = os.path.dirname(os.path.realpath(__file__))
cfg = Config(project_directory)

# subdirectory is to be used if this software is used in another site.
subdir = cfg.get_site()['subdirectory']
if subdir == 'None':
    subdir = ''

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-re-validate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure to use database
dbfile = "data.db"
db = DbHelper(cfg)

# Start the upkeep thread for renewals
if cfg.get_site()['site'] != "http://127.0.0.1:5000":
    upkeep = Upkeep(db, project_directory)

# The family class helps with family memberships
family = FamilyClass(dbfile)
# The square class helps with purchases
square = square_handler(cfg)
# The member class represents a member and has member functions.
mdb = Member(db, project_directory)
# PayLogHelper class is for logging payments.
pay_log = PayLogHelper(db)


@app.route(subdir + "/")
# @login_required
def index():
    return render_template("register.html")


@app.route(subdir + "/cost_values", methods=["GET"])
def cost_values():
    """Provides cost information for javascript functions"""
    costs = cfg.get_costs()
    costs['family_total'] = session.get('family_total', None)
    return jsonify(costs)


@app.route(subdir + "/email_verify", methods=["GET", "POST"]) # TODO update this to patch
def email_verify():
    """The user must verify the users email address to complete the registration. Validation is done with a code
    that was sent to the user"""

    if(request.method == "GET"):
        email = vcode = ""
        if "e" in request.args:
            email = request.args["e"]
        if "c" in request.args:
            vcode = request.args["c"]
        session['renew'] = False

        return render_template("email_verify.html", vcode=vcode, email=email)
    else:  #method is POST
        mem = mdb.check_email(request.form.get('email'), request.form.get('vcode'))
        return payment(mem)


@app.route(subdir + "/joad_registration", methods=["GET", "POST"])
def joad_registration():
    """Registers a user for a Junior Olympic Archery Development Session"""
    if(request.method == "GET"):
        jsdb = JoadSessions(db)
        js = jsdb.list_open()
        return render_template("joad_registration.html", rows=js)
    else:
        if not mdb.isValidEmail(request.form.get('email')):
            return apology("invalid email")
        joad_session = request.form.get('session')
        rows = mdb.find_by_email(request.form.get('email'))
        if len(rows) == 0:
            return apology("Record not found", 200)
        for row in rows:
            if row["first_name"] == request.form.get('first_name') and row["last_name"] == request.form.get('last_name'):
                d = row['dob']

                # check to see if the student is to old (over 20)
                if d.replace(year=d.year + 21) < date.today(): # student is to old.
                    return apology("Must be younger then 21 to register")
                mdb.setbyDict(row)

                if(joad_session is not "None"):
                    reg = JoadSessions(db).session_registration(row['id'], joad_session)

                    session['line_items'] = square.purchase_joad_sesion(reg['pay_code'], joad_session, row['email'])
                    session['description'] = 'JOAD Session' + joad_session
                    return redirect('process_payment')

        return render_template(("joad_registration.html"))



@app.route(subdir + "/pay_success", methods=["GET"])
def pay_success():
    """Shows the user that the payment was successful"""
    if 'description' in session:
        if session['description'][:len("membership")] == "membership":
            l = session['members'].split(',')
            # mdb = MemberDb(db)
            mem = mdb.find_by_id(l[0])
            mdb.set_member_pay_code_status(None, "member")
            if mem["fam"] is None:
                fam = ""
                mdb.expire_update(mem)
            else:
                rows = mdb.find_by_fam(mem["fam"])
                fam = ""
                for row in rows:
                    fam += f"{row['first_name']}'s membership number is {row['id']} \n"
                    mdb.expire_update(mem)

            if session.get('renew', False) is True:
                path = os.path.join(project_directory, "email_templates", "renew.html")
            else:
                path = os.path.join(project_directory, "email_templates", "join.html")

            mdb.send_email(path, "Welcome To Wooldley Park Archers", fam)

        elif session['description'][0:len("joad session")] == "joad session":
            JoadSessions(db).update_registration(session["members"], "paid", None)
    session.clear()
    return render_template("success.html", message="Your payment has been received, Thank You.")


def payment(mem):
    """This function does the payment process for some other functions."""
    if mem is not None:
        if mem['status'] == 'member' and session.get('renew', False) is False:
            return apology("payment already processed")
        session['mem_id'] = mem['id']
        s = "SELECT id, session_date from joad_session_registration where 1=0"
        if mem["fam"] is not None:
            rows = mdb.find_by_fam(mem['fam'])
            for row in rows:
                s += f" or mem_id = {row['id']}"
        else:
            s += f"or mem_id = {mem['id']}"
        js = db.execute(s)
        joad_sessions = len(js)
        session_date = ""
        if len(js) > 0:
            session_date = js[0]['session_date']

        session['line_items'] = square.purchase_membership(mem, False, joad_sessions, session_date)
        session['description'] = 'membership'
        if session['line_items'] is None:
            return apology("payment error")

        if mem["fam"] is not None and session.get('renew', False) is True:
            return render_template("renew_list.html", rows=rows)
        return redirect('process_payment')
    return apology("Error with code", 200)


@app.route(subdir + "/pin_shoot", methods=["GET", "POST"])
def pin_shoot():
    """Interface to register a pin shoot and pay for the shoot as well as pins."""
    if(request.method == "GET"):
        return render_template("pin_shoot.html", date=date.today())
    else:
        """ Get values, calculate pins, """
        ps = PinShoot(db)
        psd = ps.get_dict()
        for k,v in psd.items():
            psd[k] = request.form.get(k)
        ps.set_dict(psd)
        stars = ps.calculate_pins() - int(psd['prev_stars'])
        if stars < 0:
            stars = 0
        ps.record_shoot()
        ik = str(uuid.uuid4())

        session['line_items'] = square.purchase_joad_pin_shoot(ik, psd["shoot_date"], stars)
        session['description'] = f"pin_shoot {psd['shoot_date']} {psd['first_name']}"
        return redirect('process_payment')


@app.route(subdir + "/process_payment", methods=["GET", "POST"])
def process_payment():
    """Shows a payment page for making purchases"""
    square_cfg = cfg.get_square()
    paydict = {}
    if(request.method == "GET"):

        if square_cfg['environment'] == "production":
            paydict['pay_url'] = "https://js.squareup.com/v2/paymentform"
        else:
            paydict['pay_url'] = "https://js.squareupsandbox.com/v2/paymentform"
        paydict['app_id'] = square_cfg['application_id']
        paydict['location_id'] = square_cfg['location_id']
        rows = []
        if 'line_items' in session:
            # line_items = session['line_items']
            for row in session['line_items']:
                d = {'name': row['name'], 'quantity': int(row['quantity']),
                     'amount': int(row['base_price_money']['amount'])}
                print(f"amount {row['base_price_money']['amount']}, {int(row['base_price_money']['amount'])}")
                rows.append(d)
        return render_template("square_pay.html", paydict=paydict, rows=rows)
    elif request.method == 'POST':
        nonce = request.form.get('nonce')
        # environment = square_cfg['environment']
        ik = str(uuid.uuid4())
        # TODO figure out how best to get the order information and process it.
        response = square.nonce(ik, nonce, session['line_items'])
        print(f"payment response = {response}")
        if response is None:
            return apology("payment processing error")
        members = ""
        if 'mem_id' in session:
            mem = mdb.find_by_id(session['mem_id'])
            if mem["fam"] is None:
                members = str(session['mem_id'])
            else:
                rows = mdb.find_by_fam(mem["fam"])
                for row in rows:
                    members = members + row['id']
        description = ""
        if 'description' in session:
            description = session['description']
        session['members'] = members
        pay_log.add_square_payment(response, members, description, ik)

        return redirect('/pay_success')


@app.route(subdir + "/reg_values", methods=["GET"])
def reg_values():
    """Provides registration valuse for a javascript, to be used with renewals and family registrations"""
    reg = jsonify(session.get('registration', None))
    return reg


@app.route(subdir + "/register", methods=["GET", "POST"])
def register():
    """Register user"""
    def form_data():
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
        return reg
    if(request.method == "GET"):
        jsdb = JoadSessions(db)
        js = jsdb.list_open()
        return render_template("register.html", rows=[], joad_sessions=js)
    else:  # method is POST
        mem_id = session.get('mem_id', None)
        jsdb = JoadSessions(db)
        if session.get('renew', False):  # renewal'
            mem = mdb.find_by_id(mem_id)
            mdb.update_record(form_data())
            return payment(mem)

        else:
            reg = form_data()
            mdb.setbyDict(reg)
            joad = None

            # Preform server side validation of the inputs
            if(mdb.checkInput()):
                # Add member to database
                reg["id"] = mdb.add(family)
                if(reg['level'] == "invalid"):
                    return apology("Error in form", 200)

                # If a JOAD session was selected, check that the member is under 21,
                # if so register them for a session.
                if request.form.get('joad') is not None:
                    d = request.form.get('dob').split('-')
                    if date(int(d[0]) + 21, int(d[1]), int(d[2])) > date.today():  # student is not to old.
                        joad = JoadSessions(db).session_registration(reg['id'], request.form.get('joad'),
                                                              'see membership', None)

                if(family.fam_id is None):  # not a family registration
                    session['registration'] = None
                    return redirect("/")
                else:  # Family registration
                    if session.get("registration", None) is None:
                        path = os.path.join(project_directory, "email_templates", "verify.html")
                        mdb.send_email(path, "Email Verification Code")

                    # Calculate the running cost for the membership with the possibility of adding JOAD sessions in.
                    costs = cfg.get_costs()
                    if session.get('family_total', None) is None:
                        session['family_total'] = costs['family_membership']
                    if joad is not None:
                        session['family_total'] = session['family_total'] + costs['joad_session']

                    # clear values that will be different for family members.
                    reg["first_name"] = ""
                    reg["last_name"] = ""
                    reg["dob"] = ""
                    session['registration'] = reg

                    return render_template("register.html", rows=family.members, joad_sessions=jsdb.list_open())
            else:
                return render_template("register.html", rows=family.members, joad_sessions=jsdb.list_open())


@app.route(subdir + "/renew", methods=["GET", "POST"])
def renew():
    """Provides interface to request a renewal code by entering email address.
    Also to provide renewal verification with email address and code"""
    if(request.method == "GET"):
        print(request.args)
        email = rc = ""
        session['renew'] = True
        if "e" in request.args:
            email = request.args["e"]
        if "c" in request.args:
            rc = request.args["c"]
        return render_template("renew.html", email=email, renew_code=rc)
    else:  #  method is POST
        mem = mdb.check_email(request.form.get('email'), request.form.get('vcode'))
        if(mem['status'] != 'member'):
            return render_template("email_verify.html", vcode=request.form.get('vcode'), email=request.form.get('email'))
        mem['renewal'] = True
        session["registration"] = mem
        session['mem_id'] = mem['id']

        # If email is verified, then process renewal.
        if mem is not None:
            return render_template("register.html")
        else:
            return apology("Invalid email")


@app.route(subdir + "/renew_code", methods=["POST"])
def renew_code():
    """ send an email to the member in the database with a renewal code if that email exists.
        If valid email address is not in database do nothing.
        If the address is not an email address return invalid email."""
    # mdb = MemberDb(db)
    if (mdb.isValidEmail(request.form.get('email2'))):
        rows = mdb.find_by_email(request.form.get('email2'))
        if (len(rows) > 0):
            mdb.send_renewal(rows[0])
        return redirect("/")
    else:
        return apology("Invalid email")


@app.route(subdir + "/reset", methods=["GET", "POST"])
def reset():
    """Used to clear session data. Called from register.html when user is done with family registration."""
    family.clear()
    session["registration"] = None
    session.clear()
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
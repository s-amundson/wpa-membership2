import os
import sys
from datetime import date
import uuid

from flask import Flask, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
# from werkzeug.security import check_password_hash, generate_password_hash
from DbHelper import DbHelper
from CurrentRegistration import CurrentRegistration
from PinShoot import PinShoot

from helpers import apology, login_required
from MemberDb import MemberDb
from FamilyClass import FamilyClass
from square_handler import square_handler
from PayLogHelper import PayLogHelper
from JoadSessions import JoadSessions
from Config import Config
from Upkeep import Upkeep



# Configure application
app = Flask(__name__)
project_directory = os.path.dirname(os.path.realpath(__file__))
cfg = Config(project_directory)
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

# # Custom filter
# app.jinja_env.filters["usd"] = usdx


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#app.logger.error(f"sys.prefix {sys.prefix}")

# Configure to use database
dbfile = "data.db"
db = DbHelper(cfg)

Upkeep(db, project_directory)
current_reg = CurrentRegistration()
family = FamilyClass(dbfile)

square = square_handler(cfg)
mdb = MemberDb(db, project_directory)
pay_log = PayLogHelper(db)


@app.route(subdir + "/")
# @login_required
def index():
    return render_template("register.html")


@app.route(subdir + "/add")
@login_required
def add():
    """Add member to database"""
    return apology("TODO")


@app.route(subdir + "/cost_values", methods=["GET"])
def cost_values():
    return jsonify(cfg.get_costs())


@app.route(subdir + "/email_verify", methods=["GET", "POST"]) # TODO update this to patch
def email_verify():
    """verify the users email address with a code"""

    if(request.method == "GET"):
        print(request.args)
        email = vcode = ""
        if "e" in request.args:
            email = request.args["e"]
        if "c" in request.args:
            vcode = request.args["c"]

        # This does not comply with GET
        # if(email is not "" and vcode is not ""):
        #     if(check(email, vcode)):
        #         return render_template("email_verified.html")
        #     else:
        #         return apology("Invalid Code")  # or email already validated
        return render_template("email_verify.html", vcode=vcode, email=email)
    else:  #method is POST
        #  mdb = MemberDb(db, project_directory)
        mem = mdb.check_email(request.form.get('email'), request.form.get('vcode'))

        # If email is verified, then process payment.
        if mem is not None:
            if mem['status'] == 'member':
                return apology("payment already processed")
            session['mem_id'] = mem['id']
            session['renew'] = False
            session['line_items'] = square.purchase_membership(mem, False)
            session['description'] = 'membership'



                # line_items.append({})
                # line_items[0]['name'] = f"JOAD Session {date}"
                # line_items[0]['quantity'] = '1'
                # line_items[0]['base_price_money'] = {}
                # line_items[0]['base_price_money']['amount'] = 95 * 100
                # line_items[0]['base_price_money']['currency'] = 'USD'
            return redirect('process_payment')
        #
        #     if p is not None:
        #         mdb.square_payment(p, "membership")
        #
        #         return redirect(p["checkout"]['checkout_page_url'])
        #
        #     else:
        #         return apology("payment problem")  # or email already validated
        # else:
        #     return apology("Invalid Code")  # or email already validated


@app.route(subdir + "/joad_registration", methods=["GET", "POST"])
def joad_registration():
    if(request.method == "GET"):
        jsdb = JoadSessions(db)
        js = jsdb.list_open()
        return render_template("joad_registration.html", rows=js)
    else:
        mdb = MemberDb(db)
        if not mdb.isValidEmail(request.form.get('email')):
            return apology("invalid email")
        joad_session = request.form.get('session')
        rows = mdb.find_by_email(request.form.get('email'))
        for row in rows:
            if row["first_name"] == request.form.get('first_name') and row["last_name"] == request.form.get('last_name'):
                d = row['dob']
                print(f"application.joad_registration dob = {d} 21yo = {d.replace(year=d.year + 21)}")
                # check to see if the student is to old (over 20)
                if d.replace(year=d.year + 21) < date.today(): # student is to old.
                    return apology("Must be younger then 21 to register")
                mdb.setbyDict(row)
                mdb.joad_register()
                if(joad_session is not "None"):
                    reg = JoadSessions(db).session_registration(row['id'])
                    session['line_items'] = square.purchase_joad_sesion(reg['pay_code'], joad_session, row['email'])
                    session['description'] = 'JOAD Session' + joad_session
                    return redirect('process_payment')
                    # p = square.purchase_joad_sesion(reg['pay_code'], joad_session, row['email'])
                    # PayLogHelper(db).add_square_payment(p, row['id'], f"joad session {joad_session}")
                    #
                    # print(s)
                    # return redirect(p["checkout"]['checkout_page_url'])

                    #     return render_template("success.html", message="Thank you for registering")  # TODO change this
        return render_template(("joad_registration.html"))


@app.route(subdir + "/pay_success", methods=["GET"])
def pay_success():

    # http: // www.example.com / order - complete?checkoutId = xxxxxx & orderId = xxxxxx & referenceId = xxxxxx & transactionId = xxxxxx
    # https://wp3.amundsonca.com/?checkoutId=CBASEO3ShiHBS717uF3w9fMkzmE&page_id=9&referenceId=reference_id&transactionId=DotaTob7qJzQe1Ndj5jsUnmt3d4F

    #l = pay_log.update_payment_state(request.args)
    if 'description' in session:
        if session['description'] == "membership":
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
            path = os.path.join(project_directory, "email_templates", "join.html")
            mdb.send_email(path, "Welcome To Wooldley Park Archers", fam)
        elif session['description'][0:len("joad session")] == "joad session":
            JoadSessions(db).update_registration(session["members"], "paid", None)
    session.clear()
    return render_template("success.html", message="Your payment has been received, Thank You.")


@app.route(subdir + "/pin_shoot", methods=["GET", "POST"])
def pin_shoot():
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
        print(f"psd['stars'] = {psd['stars']}, stars = {stars}")
        if stars < 0:
            stars = 0
        ps.record_shoot()
        # plh = PayLogHelper(db)
        # pay_log = plh.create_entry("", "Pin Shoot")
        ik = str(uuid.uuid4())
        # print(pay_log)

        session['line_items'] = square.purchase_joad_pin_shoot(ik, psd["shoot_date"], stars)
        session['description'] = f"pin_shoot {psd['shoot_date']} {psd['first_name']}"
        # plh.update_payment(p, pay_log["id"])
        return redirect('process_payment')


@app.route(subdir + "/process_payment", methods=["GET", "POST"])
def process_payment():

    print(f"process_payment method = {request.method}")
    square_cfg = cfg.get_square()
    paydict = {}
    if(request.method == "GET"):

        if square_cfg['environment'] == "production":
            paydict['pay_url'] = "https://js.squareup.com/v2/paymentform"
        else:
            paydict['pay_url'] = "https://js.squareupsandbox.com/v2/paymentform"
        paydict['app_id'] = square_cfg['application_id']
        paydict['location_id'] = square_cfg['location_id']
        # print(f"payment_form_url = {pay_url}, app_id = {app_id}}, location_id = {location_id}")
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
        response = square.nonce(ik, nonce)
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
    reg = jsonify(current_reg.get_registration())
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
        return render_template("register.html", rows=js)
    else:  # method is POST
        #mdb = MemberDb(db)
        mem_id = session.get('mem_id', None)
        if session.get('renew', False):  # renewal'
            mem = mdb.find_by_id(mem_id)
            mdb.update_record(form_data())

            mem['pay_code'] = mdb.set_pay_code()
            p = square.purchase_membership(mem, session.get('renew', False))
            if p is not None:
                mdb.square_payment(p, "membership")
                return redirect(p["checkout"]['checkout_page_url'])

            print(f"session sid = {session.sid}, ")
            current_reg.set_registration(None)
            session.clear()
            return redirect('/')
        else:

            reg = form_data()
            # current_reg.set_registration(reg)
            mdb.setbyDict(reg)
            if(mdb.checkInput()):
                reg["id"] = mdb.add(family)
                if(family.fam_id is None):  # not a family registration
                    current_reg.set_registration(None)
                    # if(mem['level'] == "joad"):
                    #     return render_template("joad_add.html")
                    return redirect("/")
                else:
                    print("current_reg = {}".format(current_reg.get_registration()))
                    app.logger.info(f"current_reg = {current_reg.get_registration()}")
                    if current_reg.get_registration() is None:
                        path = os.path.join(project_directory, "email_templates", "verify.html")
                        mdb.send_email(path, "Email Verification Code")
                    reg["first_name"] = ""
                    reg["last_name"] = ""
                    reg["dob"] = ""
                    current_reg.set_registration(reg)
                    print("family.members={}".format(family.members), file=sys.stdout)
                    return render_template("register.html", rows=family.members)
            else:
                return render_template("register.html", rows=family.members)


@app.route(subdir + "/renew", methods=["GET", "POST"])
def renew():
    # to request a renewal code by entering email address. Also to provide renewal verification with email address and code
    if(request.method == "GET"):
        print(request.args)
        email = rc = ""
        if "e" in request.args:
            email = request.args["e"]
        if "c" in request.args:
            rc = request.args["c"]
        return render_template("renew.html", email=email, renew_code=rc)
    else:  #  method is POST
        #mem = MemberDb(db)
        #  TODO add renew table to track renewals (id, mem_id, renew_date)
        if(mdb.isValidEmail(request.form.get('email'))):
            rows = mdb.find_by_email(request.form.get('email'))
            if(len(rows) == 0):
                return apology("Email not found")
            elif(len(rows) == 1):
                current_reg.set_registration(rows[0])
                session['mem_id'] = rows[0]['id']
                session['renew'] = True
                print(f"Session id = {session.sid}, mem_id = {session.get('mem_id')}, renew = {session.get('renew')}")
                return render_template("register.html")
            else:
                return render_template("renew_list.html", rows=rows)
        else:
            return apology("Invalid email")

@app.route(subdir + "/renew_code", methods=["POST"])
def renew_code():
    """ send an email to the member in the database with a renewal code if that email exists.
        If valid email address is not in database do nothing."""
    # mdb = MemberDb(db)
    if (mdb.isValidEmail(request.form.get('email2'))):
        rows = mdb.find_by_email(request.form.get('email2'))
        if (len(rows) > 0):
            mdb.send_renewal(rows[0])
        return redirect("/")
    else:
        return apology("Invalid email")

@app.route(subdir + "/renew_id", methods=["GET"])
def renew_id():
    n = request.args["id"]
    print(n, file=sys.stdout)
    if(n is not None):
        #mem = MemberDb(db)
        m = mdb.find_by_id(n)
        current_reg.set_registration(m)
        if(m["fam"] is None):
            return render_template("register.html")
        else:
            rows = mdb.find_by_fam(m["fam"])
            return render_template("register.html", rows=rows)


@app.route(subdir + "/reset", methods=["GET", "POST"])
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
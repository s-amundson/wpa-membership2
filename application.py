import sys
from datetime import date

from flask import Flask, jsonify, redirect, render_template, request
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

#app.logger.error(f"sys.prefix {sys.prefix}")

# Configure to use database
dbfile = "data.db"
db = DbHelper()


current_reg = CurrentRegistration()
family = FamilyClass(dbfile)

square = square_handler()

@app.route("/")
# @login_required
def index():
    return render_template("register.html")


@app.route("/add")
@login_required
def add():
    """Add member to database"""
    return apology("TODO")


@app.route("/email_verify", methods=["GET", "POST"]) # TODO update this to patch
def email_verify():
    """verify the users email address with a code"""

    if(request.method == "GET"):
        print(request.args)
        if "e" in request.args:
            email = request.args["e"]
        if "c" in request.args:
            vcode = request.args["c"]
        # try:
        #     email = request.args["e"]
        # except:
        #     email = ""
        # try:
        #     vcode = request.args["c"]
        # except:
        #     vcode = ""
        # This does not comply with GET
        # if(email is not "" and vcode is not ""):
        #     if(check(email, vcode)):
        #         return render_template("email_verified.html")
        #     else:
        #         return apology("Invalid Code")  # or email already validated
        return render_template("email_verify.html", code=vcode, email=email)
    else:  #method is POST
        mdb = MemberDb(db)
        mem = mdb.check_email(request.form.get('email'), request.form.get('vcode'))

        # If email is verified, then process payment.
        if mem is not None:
            if mem['status'] == 'member':
                return apology("payment already processed")
            p = square.purchase_membership(mem)

            if p is not None:
                mdb.square_payment(p, "membership")

                # make link for testing purposes
                s = f"http://127.0.0.1:5000/pay_success?checkoutId={p['checkout']['id']}" \
                    f"&referenceId={p['checkout']['order']['reference_id']}" \
                    f"&transactionId={p['checkout']['order']['id']}"

                print(s)
                return redirect(p["checkout"]['checkout_page_url'])

            else:
                return apology("payment problem")  # or email already validated
        else:
            return apology("Invalid Code")  # or email already validated

@app.route("/joad_registration", methods=["GET", "POST"])
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
                    p = square.purchase_joad_sesion(reg['pay_code'], joad_session, row['email'])
                    PayLogHelper(db).add_square_payment(p, row['id'], f"joad session {joad_session}")

                    # make link for testing purposes
                    s = f"http://127.0.0.1:5000/pay_success?checkoutId={p['checkout']['id']}" \
                        f"&referenceId={p['checkout']['order']['reference_id']}" \
                        f"&transactionId={p['checkout']['order']['id']}"

                    print(s)
                    return redirect(p["checkout"]['checkout_page_url'])
                    #purchase_joad_sesion(self, idempotency_key, date, email):
                    # if mdb.joad_register(js):
                    #     return render_template("success.html", message="Thank you for registering")  # TODO change this
        return render_template(("joad_registration.html"))

@app.route("/pay_success", methods=["GET"])
def pay_success():

    # http: // www.example.com / order - complete?checkoutId = xxxxxx & orderId = xxxxxx & referenceId = xxxxxx & transactionId = xxxxxx
    # https://wp3.amundsonca.com/?checkoutId=CBASEO3ShiHBS717uF3w9fMkzmE&page_id=9&referenceId=reference_id&transactionId=DotaTob7qJzQe1Ndj5jsUnmt3d4F


    l = PayLogHelper(db).update_square_payment(request.args)
    if l['description'] == "membership":
        l = l['members'].split(',')
        mdb = MemberDb(db)
        mem = mdb.find_by_id(l[0])
        mdb.set_member_pay_code_status(None, "member")
        if (mem["fam"] is None):
            fam = ""
            mdb.expire_update(mem)
        else:
            rows = mdb.find_by_fam(mem["fam"])
            fam = ""
            for row in rows:
                fam += f"{row['first_name']}'s membership number is {row['id']} \n"
                mdb.expire_update(mem)
        mdb.send_email('email_templates/join.html', "Welcome To Wooldley Park Archers", fam)
    elif l['description'][0:len("joad session")] == "joad session":
        JoadSessions(db).update_registration(l["members"], "paid", None)

    return render_template("success.html", message="Your payment has been received, Thank You.")


@app.route("/pin_shoot", methods=["GET", "POST"])
def pin_shoot():
    if(request.method == "GET"):
        return render_template("pin_shoot.html")
    else:
        ps = PinShoot(db)
        psd = ps.get_dict()
        for k,v in psd.items():
            psd[k] = request.form.get(k)

        psd["stars"] = ps.calculate_pins(psd['category'], psd['bow'], psd['target'], psd['distance'], psd['score'])
        ps.set_dict(psd)
        ps.record_shoot()
        return apology(f"Stars = {psd['stars']}", 200)

@app.route("/reg_values", methods=["GET"])
def reg_values():
    return jsonify(current_reg.get_registration())


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if(request.method == "GET"):
        return render_template("register.html")
    else:  # method is POST
        mem = MemberDb(db)
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
                # if(mem['level'] == "joad"):
                #     return render_template("joad_add.html")
                return redirect("/")
            else:
                print("current_reg = {}".format(current_reg.get_registration()))
                app.logger.info(f"current_reg = {current_reg.get_registration()}")
                if current_reg.get_registration() is None:
                    mem.send_email("email_templates/verify.html", "Email Verification Code")
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
    # to request a renewal code by entering email address. Also to provide renewal verification with email address and code
    if(request.method == "GET"):
        return render_template("renew.html")
    else:  #  method is POST
        mem = MemberDb(db)
        #  TODO add renew table to track renewals (id, mem_id, renew_date)
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

@app.route("/renew_code", methods=["POST"])
def renew_code():
    """ send an email to the member in the database with a renewal code if that email exists.
        If valid email address is not in database do nothing."""
    mdb = MemberDb(db)
    if (mdb.isValidEmail(request.form.get('email2'))):
        rows = mdb.find_by_email(request.form.get('email2'))
        if (len(rows) > 0):
            mdb.send_renewal(rows[0])
        return redirect("/")
    else:
        return apology("Invalid email")

@app.route("/renew_id", methods=["GET"])
def renew_id():
    n = request.args["id"]
    print(n, file=sys.stdout)
    if(n is not None):
        mem = MemberDb(db)
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
import logging
from uuid import uuid4

from django.conf import settings
from django.shortcuts import render
from django.utils.datetime_safe import date
from django.views.generic.base import View

from registration.models import Joad_session_registration, Member, Payment_log

logger = logging.getLogger(__name__)


class ProcessPaymentView(View):
    """Shows a payment page for making purchases"""
    def get(self, request):
        paydict = {}
        if settings.SQUARE_CONFIG['environment'] == "production":
            paydict['pay_url'] = "https://js.squareup.com/v2/paymentform"
        else:
            paydict['pay_url'] = "https://js.squareupsandbox.com/v2/paymentform"
        paydict['app_id'] = settings.SQUARE_CONFIG['application_id']
        paydict['location_id'] = settings.SQUARE_CONFIG['location_id']
        rows, total = self.table_rows(request.session)
        bypass = False
        if settings.DEBUG:
            bypass = True

        context = {'paydict': paydict, 'rows': rows, 'total': total, 'bypass':bypass}
        return render(request, 'registration/pin_shoot.html', context)

    def nonce(self, idempotency_key, nonce, line_items):
        """Process payment with squares nonce"""
        # Every payment you process with the SDK must have a unique idempotency key.
        # If you're unsure whether a particular payment succeeded, you can reattempt
        # it with the same idempotency key without worrying about double charging
        # the buyer.
        # idempotency_key = str(uuid.uuid1())

        # get the amount form the line items
        # also get line item name and add to notes
        amt = 0
        note = ""
        for line in line_items:
            amt += line['base_price_money']['amount'] * int(line['quantity'])
            note += f" {line['name']},"

        # Monetary amounts are specified in the smallest unit of the applicable currency.
        amount = {'amount': amt, 'currency': 'USD'}

        # To learn more about splitting payments with additional recipients,
        # see the Payments API documentation on our [developer site]
        # (https://developer.squareup.com/docs/payments-api/overview).
        body = {'idempotency_key': idempotency_key, 'source_id': nonce, 'amount_money': amount}

        # not sure if line items belongs in nonce
        body['order'] = {}
        body['order']['reference_id'] = idempotency_key
        body['order']['line_items'] = line_items
        body['note'] = note

        # The SDK throws an exception if a Connect endpoint responds with anything besides
        # a 200-level HTTP code. This block catches any exceptions that occur from the request.
        api_response = self.client.payments.create_payment(body)
        if api_response.is_success():
            res = api_response.body['payment']
        elif api_response.is_error():
            res = "Exception when calling PaymentsApi->create_payment: {}".format(api_response.errors)
        print(res)
        return res

    def table_rows(self, session):
        rows = []
        total = 0
        if 'line_items' in session:
            # line_items = session['line_items']
            for row in session['line_items']:
                d = {'name': row['name'], 'quantity': int(row['quantity']),
                     'amount': int(row['base_price_money']['amount'])}
                print(f"amount {row['base_price_money']['amount']}, {int(row['base_price_money']['amount'])}")
                rows.append(d)
                total += int(row['base_price_money']['amount'])

        return rows, total

    def post(self, request):
        idempotency_key = request.session.get('idempotency_key', str(uuid4()))
        if idempotency_key is not None:
            try:
                mem = Member.objects.filter(email_code=idempotency_key)
            except Member.DoesNotExist:
                mem = None
            try:
                joad = Joad_session_registration.objects.filter(idempotency_key=idempotency_key)
            except:
                joad = None
        if not settings.DEBUG:
            nonce = request.POST.get('nonce')

            # environment = square_cfg['environment']
            square_response = self.nonce(idempotency_key, nonce, request.session['line_items'])
            if isinstance(square_response, str):
                return render(request, 'registration/message.html', {'message': 'payment processing error'})
            # if response.is_error():
            logging.debug(f"response type = {type(square_response)} response = {square_response}")

        members = ""
        for m in mem:
            members = members + f"{m['id']}, "
        # if 'mem' in request.session:
        #     mem = request.session['mem']
        #     if mem["fam"] is None:
        #         members = f"{mem['id']}, "
        #     else:
        #         rows = mdb.find_by_fam(mem["fam"])
        #         for row in rows:
        #             members = members + f"{row['id']}, "
        #     email = mem['email']
        if 'email' in request.session:
            mem = None
            email = request.session['email']
        description = request.session['line_items']['name']
        # if 'description' in session:
        #     description = session['description']
        # session['members'] = members
        subject = ""
        template = "email/purchase_email.html"
        # mem = None
        fam = []
        receipt = ""

        #     members = models.CharField(max_length=50, null=True)
        #     reg_date = models.DateField()
        #     checkout_created_time = models.DateTimeField()
        #     checkout_id = models.CharField(max_length=50, null=True)
        #     order_id = models.CharField(max_length=50, null=True)
        #     location_id = models.CharField(max_length=50, null=True)
        #     state = models.CharField(max_length=20, null=True)
        #     total_money = models.CharField(max_length=50, null=True)
        #     description = models.CharField(max_length=50, null=True)
        #     idempotency_key = models.UUIDField()
        #     receipt = models.CharField(max_length=100, null=True)

        if not settings.DEBUG:
            # cd = dateutil.parser.parse(square_response['created_at']).strftime('%Y-%m-%d %H:%M:%S')
            cd = date.fromisoformat(square_response['created_at'])
            Payment_log.objects.create(members=members,
                                       checkout_created_time=cd,
                                       checkout_id=square_response['id'],
                                       order_id=square_response['order_id'],
                                       location_id=square_response['location_id'],
                                       state=square_response['status'],
                                       total_money=square_response['amount_money']['amount'],
                                       description=description,
                                       idempotency_key=idempotency_key,
                                       receipt=square_response['receipt_url']
                                       )

            receipt = f"Link to reciept: {square_response['receipt_url']}"

        if description[:len("JOAD Pin Shoot")] == 'JOAD Pin Shoot':
            subject = 'Pin Shoot Payment Confirmation'

        # elif description[:len('JOAD Session')] == 'JOAD Session':
        #     if 'joad_session' in session:
        #         subject = 'JOAD Session Payment Confirmation'
        #
        #         # elif session['description'][0:len("joad session")] == "joad session":
        #         # JoadSessions(db).update_registration(mem["id"], "paid", None, session['joad_session'])
        #         JoadSessions(db).update_status_by_paycode('paid', mem['email_code'])
        #
        # elif description == 'membership':
        #     # l = session['members'].split(',')
        #     # mdb = MemberDb(db)
        #     # mem = mdb.find_by_id(l[0])
        #
        #     fam = []
        #     template = 'email/join.html'
        #     JoadSessions(db).update_status_by_paycode('paid', mem['email_code'])
        #     # s = f"UPDATE member SET `email_code` = %s, `status` = 'member' WHERE `email_code`` = '{mem['email_code']}'"
        #     # db.execute(s)
        #
        #     if mem["fam"] is None:
        #         mdb.expire_update(mem)
        #         # mdb.set_member_pay_code_status(None, "member")
        #     else:
        #         rows = mdb.find_by_fam(mem["fam"])
        #         for row in rows:
        #             fam.append(f"{row['first_name']}'s membership number is {row['id']}")
        #             mdb.expire_update(row)
        #             # mdb.set_member_pay_code_status(None, "member")
        #
        #     if session.get('renew', False) is True:
        #         # path = os.path.join(project_directory, "email_templates", "renew.html")
        #         # TODO this is not the correct template for this.
        #         subject = 'Renew'
        #
        #     else:
        #         subject = 'Welcome To Wooldley Park Archers'

            # mdb.send_email(path, "Welcome To Wooldley Park Archers", fam)
        # email_helper.payment_email(email, subject, template, table_rows(), mem, fam, receipt)
        return render(request, 'registration/message.html', {'message': 'payment successful'})
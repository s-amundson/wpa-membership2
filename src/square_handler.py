from square.client import Client
from Config import Config


class square_handler:

    def __init__(self, cfg):
        # Get config settings
        self.cfg = cfg.get_square()
        self.site = cfg.get_site()['site']

        # Create an instance of the API Client
        # and initialize it with the credentials
        # for the Square account whose assets you want to manage

        self.client = Client(
            access_token=self.cfg["access_token"],
            environment=self.cfg["environment"],
        )
        self.checkout_api = self.client.checkout
    def nonce(self, idempotency_key, nonce):
        # Every payment you process with the SDK must have a unique idempotency key.
        # If you're unsure whether a particular payment succeeded, you can reattempt
        # it with the same idempotency key without worrying about double charging
        # the buyer.
        # idempotency_key = str(uuid.uuid1())

        # Monetary amounts are specified in the smallest unit of the applicable currency.
        # This amount is in cents. It's also hard-coded for $1.00, which isn't very useful.
        amount = {'amount': 100, 'currency': 'USD'}

        # To learn more about splitting payments with additional recipients,
        # see the Payments API documentation on our [developer site]
        # (https://developer.squareup.com/docs/payments-api/overview).
        body = {'idempotency_key': idempotency_key, 'source_id': nonce, 'amount_money': amount}

        # The SDK throws an exception if a Connect endpoint responds with anything besides
        # a 200-level HTTP code. This block catches any exceptions that occur from the request.
        api_response = self.client.payments.create_payment(body)
        if api_response.is_success():
            res = api_response.body['payment']
        elif api_response.is_error():
            res = "Exception when calling PaymentsApi->create_payment: {}".format(api_response.errors)
        print(res)

    def order(self, idempotency_key, line_items, email, redirect_url):
        location_id = self.cfg["location_id"]
        body = {}
        body['idempotency_key'] = str(idempotency_key)
        body['order'] = {}
        body['order']['reference_id'] = str(idempotency_key)
        body['order']['line_items'] = line_items
        if email is not None:
            body['pre_populate_buyer_email'] = email
        body['merchant_support_email'] = 'wpa4membership@gmail.com'
        # TODO change redirect.
        body['redirect_url'] = redirect_url

        result = self.checkout_api.create_checkout(location_id, body)
        if result.is_success():
            # mem.square_payment(self, result)
            return result.body
        elif result.is_error():
            print(result.errors)
        return None

    def purchase_joad_sesion(self, idempotency_key, date, email):
        print(f"square_handler.purchase_joad_session ik = {idempotency_key}, date = {date}, email = {email}")
        line_items = []
        line_items.append({})
        line_items[0]['name'] = f"JOAD Session {date}"
        line_items[0]['quantity'] = '1'
        line_items[0]['base_price_money'] = {}
        line_items[0]['base_price_money']['amount'] = 95 * 100
        line_items[0]['base_price_money']['currency'] = 'USD'
        redirect_url = f'{self.site}/pay_success'
        return self.order(idempotency_key, line_items, email,redirect_url)

    def purchase_joad_pin_shoot(self, idempotency_key, date, email, qty):
        print(f"square_handler.purchase_joad_session ik = {idempotency_key}, date = {date}, email = {email}")
        line_items = []
        line_items.append({})
        line_items[0]['name'] = f"JOAD Pin Shoot {date}"
        line_items[0]['quantity'] = '1'  # string?
        line_items[0]['base_price_money'] = {}
        line_items[0]['base_price_money']['amount'] = 15 * 100
        line_items[0]['base_price_money']['currency'] = 'USD'

        line_items.append({})
        line_items[1]['name'] = f"JOAD Pins {date}"
        line_items[1]['quantity'] = str(qty)  # string?
        line_items[1]['base_price_money'] = {}
        line_items[1]['base_price_money']['amount'] = 5 * 100 * qty
        line_items[1]['base_price_money']['currency'] = 'USD'
        redirect_url = f'{self.site}/pay_success'
        print(f"square_handler.purchase_joad_session line_items = {line_items}, url = {redirect_url}")
        return self.order(idempotency_key, line_items, email, redirect_url)

    def purchase_membership(self, mem, renew):
        if mem['benefactor']:
            price = 100
            mem['level'] = "benefactor"
        else:
            if mem['level'] == "standard":
                price = 20
            elif mem['level'] == "family":
                price = 40
            elif mem['level'] == "joad":
                price = 18
            elif mem['level'] == "senior":
                price = 18
            else:
                return None

        line_items = []

        line_items.append({})
        if renew:
            line_items[0]['name'] = f"{mem['level']} Membership Renewal"
        else:
            line_items[0]['name'] = f"{mem['level']} Membership"
        line_items[0]['quantity'] = '1'
        line_items[0]['base_price_money'] = {}
        line_items[0]['base_price_money']['amount'] = price * 100
        line_items[0]['base_price_money']['currency'] = 'USD'
        return line_items
        # redirect_url = f'{self.site}/pay_success'
        # return self.order(str(mem['pay_code']), line_items, mem['email'], redirect_url)


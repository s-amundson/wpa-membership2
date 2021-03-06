from square.client import Client
from Config import Config


class square_handler:
    """Helper class for handling square payments"""
    def __init__(self, cfg):
        # Get config settings
        self.cfg = cfg.get_square()
        self.site = cfg.get_site()['site']
        self.costs = cfg.get_costs()

        # Create an instance of the API Client
        # and initialize it with the credentials
        # for the Square account whose assets you want to manage

        self.client = Client(
            access_token=self.cfg["access_token"],
            environment=self.cfg["environment"],
        )
        self.checkout_api = self.client.checkout


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

    # def order(self, idempotency_key, line_items, email, redirect_url):
    #     location_id = self.cfg["location_id"]
    #     body = {}
    #     body['idempotency_key'] = str(idempotency_key)
    #     body['order'] = {}
    #     body['order']['reference_id'] = str(idempotency_key)
    #     body['order']['line_items'] = line_items
    #     if email is not None:
    #         body['pre_populate_buyer_email'] = email
    #     body['merchant_support_email'] = 'wpa4membership@gmail.com'
    #     # TODO change redirect.
    #     body['redirect_url'] = redirect_url
    #
    #     result = self.checkout_api.create_checkout(location_id, body)
    #     if result.is_success():
    #         # mem.square_payment(self, result)
    #         return result.body
    #     elif result.is_error():
    #         print(result.errors)
    #     return None

    def purchase_joad_sesion(self, idempotency_key, date, email):
        """Creates line items for JOAD session purchase"""
        print(f"square_handler.purchase_joad_session ik = {idempotency_key}, date = {date}, email = {email}")
        line_items = []
        line_items.append({})
        line_items[0]['name'] = f"JOAD Session {date}"
        line_items[0]['quantity'] = '1'
        line_items[0]['base_price_money'] = {}
        line_items[0]['base_price_money']['amount'] = self.costs['joad_session'] * 100
        line_items[0]['base_price_money']['currency'] = 'USD'
        return line_items
        # redirect_url = f'{self.site}/pay_success'
        # return self.order(idempotency_key, line_items, email,redirect_url)

    def purchase_joad_pin_shoot(self, idempotency_key, date, qty):
        """Creates line items for JOAD pin shoot purchase"""
        print(f"square_handler.purchase_joad_session ik = {idempotency_key}, date = {date}, qty = {qty}")
        line_items = [{}]
        line_items[0]['name'] = f"JOAD Pin Shoot {date}"
        line_items[0]['quantity'] = '1'  # string?
        line_items[0]['base_price_money'] = {}
        line_items[0]['base_price_money']['amount'] = self.costs['pin_shoot'] * 100
        line_items[0]['base_price_money']['currency'] = 'USD'

        if qty > 0:
            line_items.append({})
            line_items[1]['name'] = f"JOAD Pins {date}"
            line_items[1]['quantity'] = str(qty)  # string?
            line_items[1]['base_price_money'] = {}
            line_items[1]['base_price_money']['amount'] = self.costs['joad_pin'] * 100 * qty
            line_items[1]['base_price_money']['currency'] = 'USD'
        return line_items


    def purchase_membership(self, mem, renew, joad_sessions=0, joad_date=""):
        """Creates line items for membership that can include a JOAD session"""
        if mem['benefactor']:
            price = self.costs['benefactor']
            mem['level'] = "benefactor"
        else:
            if mem['level'] == "standard":
                price = self.costs['standard_membership']
            elif mem['level'] == "family":
                price = self.costs['family_membership']
            elif mem['level'] == "joad":
                price = self.costs['joad_membership']
            elif mem['level'] == "senior":
                price = self.costs['senior_membership']
            else:
                return None

        line_items = []

        line_items.append({})
        if renew:
            line_items[0]['name'] = f"{str(mem['level']).capitalize()} Membership Renewal"
        else:
            line_items[0]['name'] = f"{str(mem['level']).capitalize()} Membership"
        line_items[0]['quantity'] = '1'
        line_items[0]['base_price_money'] = {}
        line_items[0]['base_price_money']['amount'] = price * 100
        line_items[0]['base_price_money']['currency'] = 'USD'

        if joad_sessions > 0:
            line_items.append({})
            line_items[1]['name'] = f"JOAD Session {joad_date}"
            line_items[1]['quantity'] = str(joad_sessions)
            line_items[1]['base_price_money'] = {}
            line_items[1]['base_price_money']['amount'] = self.costs['joad_session'] * 100
            line_items[1]['base_price_money']['currency'] = 'USD'
        return line_items

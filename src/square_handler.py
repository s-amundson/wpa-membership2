from square.client import Client
from Config import Config


class square_handler:

    def __init__(self):
        # Get config settings
        c = Config()
        self.cfg = c.get_square()
        self.site = c.get_site()

        # Create an instance of the API Client
        # and initialize it with the credentials
        # for the Square account whose assets you want to manage

        self.client = Client(
            access_token=self.cfg["access_token"],
            environment=self.cfg["environment"],
        )
        self.checkout_api = self.client.checkout

    # # Get an instance of the Square API you want call
    # api_locations = client.locations
    #
    # # Call list_locations method to get all locations in this Square account
    # result = api_locations.list_locations()
    # # Call the success method to see if the call succeeded
    # if result.is_success():
    #     # The body property is a list of locations
    #     locations = result.body['locations']
    #     # Iterate over the list
    #     for location in locations:
    #         # Each location is represented as a dictionary
    #         for key, value in location.items():
    #             print(f"{key} : {value}")
    #         print("\n")
    # # Call the error method to see if the call failed
    # elif result.is_error():
    #     print('Error calling LocationsApi.listlocations')
    #     errors = result.errors
    #     # An error is returned as a list of errors
    #     for error in errors:
    #         # Each error is represented as a dictionary
    #         for key, value in error.items():
    #             print(f"{key} : {value}")
    #         print("\n")
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
        line_items = [{}, {}]
        # line_items.append({})
        line_items[0]['name'] = f"JOAD Pin Shoot {date}"
        line_items[0]['quantity'] = '1'  # string?
        line_items[0]['base_price_money'] = {}
        line_items[0]['base_price_money']['amount'] = 15 * 100
        line_items[0]['base_price_money']['currency'] = 'USD'

        line_items[1]['name'] = f"JOAD Pins {date}"
        line_items[0]['quantity'] = qty  # string?
        line_items[0]['base_price_money'] = {}
        line_items[0]['base_price_money']['amount'] = 5 * 100
        line_items[0]['base_price_money']['currency'] = 'USD'
        redirect_url = f'{self.site}/pay_success'
        return self.order(idempotency_key, line_items, email, redirect_url)

    def purchase_membership(self, mem):
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

        # location_id = self.cfg["location_id"]
        # body = {}
        # body['idempotency_key'] = str(mem['pay_code'])
        # body['order'] = {}
        # body['order']['reference_id'] = str(mem['pay_code'])
        line_items = []

        line_items.append({})
        line_items[0]['name'] = f"{mem['level']} Membership"
        line_items[0]['quantity'] = '1'
        line_items[0]['base_price_money'] = {}
        line_items[0]['base_price_money']['amount'] = price * 100
        line_items[0]['base_price_money']['currency'] = 'USD'

        # body['pre_populate_buyer_email'] = mem['email']
        # body['merchant_support_email'] = 'wpa4membership@gmail.com'
        # # TODO change redirect.
        # body['redirect_url'] = f'{self.site}/pay_success'
        #
        # result = self.checkout_api.create_checkout(location_id, body)
        #
        # if result.is_success():
        #     # mem.square_payment(self, result)
        #     return result.body
        # elif result.is_error():
        #     print(result.errors)
        # return None
        redirect_url = f'{self.site}/pay_success'
        return self.order(str(mem['pay_code']), line_items, mem['email'], redirect_url)

# body['order']['line_items'][2]['discounts'].append({})
# body['order']['line_items'][2]['discounts'][0]['name'] = '$11 off Customer Discount'


# body['order']['taxes'] = []
#
# body['order']['taxes'].append({})
# body['order']['taxes'][0]['name'] = 'Sales Tax'
# body['order']['taxes'][0]['percentage'] = '8.5'
#
# body['order']['discounts'] = []
#
# body['order']['discounts'].append({})
# body['order']['discounts'][0]['name'] = 'Father\'s day 12% OFF'
# body['order']['discounts'][0]['percentage'] = '12'
#
# # body['order']['discounts'].append({})
# # body['order']['discounts'][1]['name'] = 'Global Sales $55 OFF'
# # body['order']['discounts'][1]['amount_money'] = 55
#
# body['ask_for_shipping_address'] = True
# body['merchant_support_email'] = 'merchant+support@website.com'
# body['pre_populate_buyer_email'] = 'example@email.com'
# body['pre_populate_shipping_address'] = {}
# body['pre_populate_shipping_address']['address_line_1'] = '1455 Market St.'
# body['pre_populate_shipping_address']['address_line_2'] = 'Suite 600'
# body['pre_populate_shipping_address']['locality'] = 'San Francisco'
# body['pre_populate_shipping_address']['administrative_district_level_1'] = 'CA'
# body['pre_populate_shipping_address']['postal_code'] = '94103'
# body['pre_populate_shipping_address']['country'] = 'US'
# body['pre_populate_shipping_address']['first_name'] = 'Jane'
# body['pre_populate_shipping_address']['last_name'] = 'Doe'
# body['redirect_url'] = 'https://wp3.amundsonca.com/?page_id=9'

#
# {'checkout': {
#     'ask_for_shipping_address': False,
#     'checkout_page_url': 'https://connect.squareupsandbox.com/v2/checkout?c=CBASEFoazxRYW5-AUqUSuzmnxnE&l=SVM1F73THA9W6',
#     'created_at': '2020-02-19T01:29:22Z',
#     'id': 'CBASEFoazxRYW5-AUqUSuzmnxnE',
#     'merchant_support_email': 'wpa4membership@gmail.com',
#     'order': {'created_at': '2020-02-19T01:29:22.163Z',
#               'id': 'VVDIxW91FUY8U4nzgTb1uin9Mc4F',
#               'line_items': [{
#                   'base_price_money': {'amount': 2000, 'currency': 'USD'},
#                   'gross_sales_money': {'amount': 2000, 'currency': 'USD'},
#                   'name': 'standard Membership',
#                   'quantity': '1',
#                   'total_discount_money': {'amount': 0, 'currency': 'USD'},
#                   'total_money': {'amount': 2000, 'currency': 'USD'},
#                   'total_tax_money': {'amount': 0, 'currency': 'USD'},
#                   'uid': 'fzdvzfDDHsglnujxtbZlbB',
#                   'variation_total_price_money': {'amount': 2000, 'currency': 'USD'}}],
#               'location_id': 'SVM1F73THA9W6',
#               'net_amounts': {
#                   'discount_money': {
#                       'amount': 0,
#                       'currency': 'USD'
#                   },
#                   'service_charge_money': {
#                       'amount': 0,
#                       'currency': 'USD'
#                   },
#                   'tax_money': {'amount': 0, 'currency': 'USD'},
#                   'tip_money': {'amount': 0, 'currency': 'USD'},
#                   'total_money': {'amount': 2000, 'currency': 'USD'}
#               # }, 'reference_id': 'reference_id', 'source': {'name': 'Sandbox for sq0idp-HSmCO3CJMh-XD_fhwK6EFg'}, 'state': 'OPEN', 'total_discount_money': {'amount': 0, 'currency': 'USD'}, 'total_money': {'amount': 2000, 'currency': 'USD'}, 'total_service_charge_money': {'amount': 0, 'currency': 'USD'}, 'total_tax_money': {'amount': 0, 'currency': 'USD'}, 'total_tip_money': {'amount': 0, 'currency': 'USD'}, 'updated_at': '2020-02-19T01:29:22.163Z', 'version': 1}, 'redirect_url': 'https://wp3.amundsonca.com/?page_id=9'}}

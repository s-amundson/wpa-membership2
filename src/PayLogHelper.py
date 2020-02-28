import dateutil.parser
import uuid

class PayLogHelper:
    def __init__(self, db):
        self.db = db

    def add_square_payment(self, square_result, members, description):
        """Adds a record for a square payment if not already present. Returns the state of the payment.
        This is used to prevent double payment. """
        checkout = square_result["checkout"]
        order = checkout['order']
        s = f"SELECT * FROM payment_log WHERE `checkout_id` = '{order['id']}'"
        if len(self.db.execute(s)) == 0:
            cd = dateutil.parser.parse(checkout['created_at']).strftime('%Y-%m-%d %H:%M:%S')
            od = dateutil.parser.parse(order['created_at']).strftime('%Y-%m-%d %H:%M:%S')

            s = "INSERT INTO payment_log (members, checkout_created_time, checkout_id, " \
                "order_id, order_create_time, location_id, state, total_money, description) VALUES ( "

            s += f"'{members}', '{cd}', '{checkout['id']}', '{order['id']}', " \
                 f"'{od}', '{order['location_id']}', '{order['state']}', " \
                 f"'{order['total_money']['amount']}', '{description}')"
            self.db.execute(s)
        return(order['state'])

    def create_entry(self, members, description):
        uid = uuid.uuid4()
        s = f"INSERT INTO payment_log (members, description, idempotency_key) VALUES " \
            f"({members}, {description}, {str(uid)})"
        self.db.execute(s)
        r = self.db.execute(f"SELECT * FROM `payment_log` WHERE 'idempotency_key' = {str(uid)}")
        return r

    def update_payment(self, square_result, record_id):
        checkout = square_result["checkout"]
        order = checkout['order']

        cd = dateutil.parser.parse(checkout['created_at']).strftime('%Y-%m-%d %H:%M:%S')
        od = dateutil.parser.parse(order['created_at']).strftime('%Y-%m-%d %H:%M:%S')

        s = f"UPDATE `payment_log` SET `checkout_created_time` = '{cd}', `checkout_id` = '{checkout['id']}', " \
            f"`order_id` = '{order['id']}', `order_create_time` = '{od}', `location_id` = '{order['location_id']}', " \
            f"`state` = '{order['state']}', `total_money` = '{order['total_money']['amount']}' WHERE `id` = {record_id}"

        self.db.execute(s)

    def update_payment_state(self, args):
        """Updates a record in the database"""
        s = f"UPDATE payment_log SET `state` = 'COMPLETED' WHERE `checkout_id` = '{args['checkoutId']}' and " \
            f"order_id = '{args['transactionId']}'"
        self.db.execute(s)
        s = f"SELECT * from payment_log WHERE `checkout_id` = '{args['checkoutId']}' and " \
            f"order_id = '{args['transactionId']}'"
        return self.db.execute(s)[0]


        # c = {'checkout': {'ask_for_shipping_address': False,
        #                   'checkout_page_url': 'https://connect.squareupsandbox.com/v2/checkout?c=CBASEKv2-G2nf8jv3eGAsP-64gI&l=SVM1F73THA9W6',
        #                   'created_at': '2020-02-14T04:53:20Z',
        #                   'id': 'CBASEKv2-G2nf8jv3eGAsP-64gI',
        #                   'order': {'created_at': '2020-02-14T04:53:20.702Z',
        #                             'id': '3m76uzYoU3w86U7HKKUGvIJtGi4F',
        #                             'line_items': [{'base_price_money': {'amount': 20, 'currency': 'USD'},
        #                                             'gross_sales_money': {'amount': 20, 'currency': 'USD'},
        #                                             'name': 'standard Membership', 'quantity': '1',
        #                                             'total_discount_money': {'amount': 0, 'currency': 'USD'},
        #                                             'total_money': {'amount': 20, 'currency': 'USD'},
        #                                             'total_tax_money': {'amount': 0, 'currency': 'USD'},
        #                                             'uid': 'WDLQfGW9zePThccjk5KnP',
        #                                             'variation_total_price_money': {'amount': 20, 'currency': 'USD'}}],
        #                             'location_id': 'SVM1F73THA9W6',
        #                             'net_amounts': {'discount_money': {'amount': 0, 'currency': 'USD'},
        #                                             'service_charge_money': {'amount': 0, 'currency': 'USD'},
        #                                             'tax_money': {'amount': 0, 'currency': 'USD'},
        #                                             'tip_money': {'amount': 0, 'currency': 'USD'},
        #                                             'total_money': {'amount': 20, 'currency': 'USD'}},
        #                             'reference_id': 'reference_id',
        #                             'source': {'name': 'Sandbox for sq0idp-HSmCO3CJMh-XD_fhwK6EFg'},
        #                             'state': 'OPEN',
        #                             'total_discount_money': {'amount': 0, 'currency': 'USD'},
        #                             'total_money': {'amount': 20, 'currency': 'USD'},
        #                             'total_service_charge_money': {'amount': 0, 'currency': 'USD'},
        #                             'total_tax_money': {'amount': 0, 'currency': 'USD'},
        #                             'total_tip_money': {'amount': 0, 'currency': 'USD'},
        #                             'updated_at': '2020-02-14T04:53:20.702Z', 'version': 1
        #                             }
        #                   }
        #      }
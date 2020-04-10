import dateutil.parser
import uuid

class PayLogHelper:
    def __init__(self, db):
        self.db = db

    def add_square_payment(self, square_result, members, description, idempotency_key):
        """Adds a record for a square payment if not already present. Returns the state of the payment.
        This is used to prevent double payment. """

        sql = f"SELECT * FROM payment_log WHERE `checkout_id` = '{square_result['id']}'"
        if len(self.db.execute(sql)) == 0:
            cd = dateutil.parser.parse(square_result['created_at']).strftime('%Y-%m-%d %H:%M:%S')

            sql = "INSERT INTO payment_log (members, checkout_created_time, checkout_id, " \
                "order_id, location_id, state, total_money, description) VALUES ( "

            sql += f"'{members}', '{cd}', '{square_result['id']}', '{square_result['order_id']}', " \
                 f"'{square_result['location_id']}', '{square_result['status']}', " \
                 f"'{square_result['amount_money']['amount']}', '{description}')"
            self.db.execute(sql)
        return(square_result['status'])

    def create_entry(self, members, description):
        """Creates a log entry and returns the entry"""
        uid = uuid.uuid4()
        s = f"INSERT INTO payment_log (members, description, idempotency_key) VALUES " \
            f"('{members}', '{description}', '{str(uid)}')"
        self.db.execute(s)
        r = self.db.execute(f"SELECT * FROM `payment_log` WHERE `idempotency_key` = '{str(uid)}'")
        if len(r) > 0:
            return r[0]
        else:
            return None

    def update_payment(self, square_result, record_id):
        """Updates a log entry"""
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

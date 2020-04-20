import uuid


class JoadSessions:
    """Helper class for Joad Sessions handles database interaction"""
    def __init__(self, db):
        self.db = db

    def list_open(self):
        """Returns a list of open sessions"""
        s = "SELECT * FROM `joad_sessions` WHERE `state` = 'open'"
        return self.db.execute(s)


    def session_registration(self, mem_id, session_date, pay_status='start payment', pay_code=str(uuid.uuid4())):
        """Adds a record in the database for a registrant"""

        select = f"SELECT * FROM joad_session_registration where `mem_id` = '{mem_id}' " \
                 f"AND  `session_date` = '{session_date}'"
        row = self.db.execute(select)
        if(len(row) == 0):
            s = f"INSERT INTO joad_session_registration (mem_id, pay_status, pay_code, session_date) " \
                f"VALUES ('{mem_id}', '{pay_status}', '{pay_code}', '{session_date}')"
            self.db.execute(s)
            row = self.db.execute(select)[0]
        else:
            row = row[0]
        return row


    def update_registration(self, mem_id, status, pay_code, session):
        """Updates a database registrant"""
        s = f"UPDATE joad_session_registration SET `pay_status` = '{status}', `pay_code` = %s WHERE " \
            f"`mem_id` = {mem_id} AND `session_date` = '{session}'"
        self.db.execute(s, args=(pay_code,))

    def update_status_by_paycode(self, status, pay_code):
        """Updates a database registrant"""
        s = f"UPDATE joad_session_registration SET `pay_status` = '{status}', `pay_code` = %s WHERE " \
            f"`pay_code` = %s"
        self.db.execute(s, args=(None, pay_code))

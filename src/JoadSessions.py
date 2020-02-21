import uuid

class JoadSessions:
    def __init__(self, db):
        self.db = db

    def list_open(self):
        s = "SELECT * FROM `joad_sessions` WHERE `state` = 'open'"
        return self.db.execute(s)
    def session_registration(self, mem_id):
        select = f"SELECT * FROM joad_session_registrtion where `mem_id` = '{mem_id}'"
        row = self.db.execute(select)[0]
        if(len(row) == 0):
            s = f"INSERT INTO joad_session_registration (mem_id, pay_status, pay_code) " \
                f"VALUES ('{mem_id}', 'start payment', '{str(uuid.uuid4())}'"
            self.db.execute(s)
            row = self.db.execute(select)[0]
        return row

  # `id` INT NOT NULL AUTO_INCREMENT,
  # `mem_id` int(11) NOT NULL,
  # `pay_status` varchar(20) DEFAULT NULL,
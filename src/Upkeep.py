import threading
from datetime import datetime
import time
from MemberDb import MemberDb


class Upkeep(threading.Thread):
    def __init__(self, db, project_directory):
        threading.Thread.__init__(self)
        self.stopped = threading.Event()
        print("upkeep __init__")
        self.db = db
        # self.project_directory = project_directory
        self.member = MemberDb(db, project_directory)
        self.check_time = datetime.now()
        self.start()



    def renew_email(self):
        d = 15
        s = f"SELECT * from mem2.member WHERE exp_date = DATE_ADD(CURRENT_DATE(),INTERVAL {d} DAY)"
        rows = self.db.execute(s)
        print(f"Upkeep rows={rows}")
        if len(rows) > 0:
            for row in rows:
                s = f"SELECT * from renewal_email_log WHERE mem_id = {row['id']} and DATE(sent_timestamp) = CURRENT_DATE()"
                r = self.db.execute(s)
                if len(r) == 0:
                    print("Upkeep send renewal")
                    self.member.send_renewal(row)
                    self.db.execute(f"INSERT INTO renewal_email_log ( mem_id ) VALUES ({row['id']})")


    def run(self):
        while not self.stopped.wait(5):
            if self.check_time < datetime.now():
                self.renew_email()
                self.check_time = self.check_time.replace(day=self.check_time.day + 1)

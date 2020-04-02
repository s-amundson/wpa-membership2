import threading
import time
from MemberDb import MemberDb



class Upkeep:
    def __init__(self, db, project_directory):
        self.db = db
        # self.project_directory = project_directory
        self.member = MemberDb(db, project_directory)
        self.renew_thread = threading.Thread(target=self.renew_email).start()
        # self.renew_email()

    def renew_email(self):
        while True:
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
            # Sleep for a day
            time.sleep(60 * 60 * 24)  # seconds * minutes * hours

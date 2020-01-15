import configparser

class Config:
    def __init__(self):
        self.cfg = configparser.ConfigParser()
        self.cfg.read('static/settings.cfg')
        self.sections = self.cfg.sections()
        self.sections
        self.email = {"user": self.cfg["smtp"]["user"], "password": self.cfg["smtp"]["password"],
                      "server": self.cfg["smtp"]["server"]}


    def get_smtp(self):
        return self.email
    def get_database(self):
        pass


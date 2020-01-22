import configparser

class Config:
    def __init__(self):
        self.cfg = configparser.ConfigParser()
        self.cfg.read('static/settings.cfg')
        self.sections = self.cfg.sections()

        self.database = {}
        for key in self.cfg["database"]:
            self.database[key] = self.cfg["database"][key]

        self.email = {}
        for key in self.cfg["smtp"]:
            self.database[key] = self.cfg["smtp"][key]

        # {"user": self.cfg["smtp"]["user"], "password": self.cfg["smtp"]["password"],
        #               "server": self.cfg["smtp"]["server"]}

    def get_database(self):
        return self.database


    def get_smtp(self):
        return self.email


if __name__ == '__main__':
    Config()
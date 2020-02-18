import configparser

class Config:
    def __init__(self):
        self.cfg = configparser.ConfigParser()
        self.cfg.read('static/settings.cfg')
        self.sections = self.cfg.sections()

    def get_database(self):
        database = {}
        for key in self.cfg["database"]:
            database[key] = self.cfg["database"][key]
        return database

    def get_smtp(self):
        email = {}
        for key in self.cfg["smtp"]:
            email[key] = self.cfg["smtp"][key]
        return email

    def get_square(self):
        square = {}
        for key in self.cfg["square"]:
            square[key] = self.cfg["square"][key]
        return square

if __name__ == '__main__':
    Config()
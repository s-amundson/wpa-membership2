import configparser
import os


class Config:

    def __init__(self, project_directory):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(os.path.join(project_directory, "static", "settings.cfg"))
        self.sections = self.cfg.sections()
        print(self.sections)


    def get_costs(self):
        costs = {}
        for key in self.cfg["costs"]:
            costs[key] = int(self.cfg["costs"][key])
        return costs

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

    def get_site(self):
        main = {}
        print(self.cfg["main"])
        for key in self.cfg["main"]:
            main[key] = self.cfg["main"][key]
        return main

    def get_square(self):
        square = {}
        for key in self.cfg["square"]:
            square[key] = self.cfg["square"][key]
        return square

if __name__ == '__main__':
    Config()
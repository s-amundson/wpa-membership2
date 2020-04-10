import configparser
import os


class Config:
    """ Gets the configuration settings from settings.cfg. Provides functions to get dicts for each heading"""
    def __init__(self, project_directory):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(os.path.join(project_directory, "static", "settings.cfg"))
        self.sections = self.cfg.sections()

    def get_costs(self):
        """Returns a dictionary of the costs"""
        costs = {}
        for key in self.cfg["costs"]:
            costs[key] = int(self.cfg["costs"][key])
        return costs

    def get_database(self):
        """Returns a dictionary of the database settings"""
        database = {}
        for key in self.cfg["database"]:
            database[key] = self.cfg["database"][key]
        return database

    def get_smtp(self):
        """Returns a dictionary of the email settings"""
        email = {}
        for key in self.cfg["smtp"]:
            email[key] = self.cfg["smtp"][key]
        return email

    def get_site(self):
        """Returns a dictionary of the site settings"""
        main = {}
        print(self.cfg["main"])
        for key in self.cfg["main"]:
            main[key] = self.cfg["main"][key]
        return main

    def get_square(self):
        """Returns a dictionary of the square settings"""
        square = {}
        for key in self.cfg["square"]:
            square[key] = self.cfg["square"][key]
        return square

if __name__ == '__main__':
    Config()
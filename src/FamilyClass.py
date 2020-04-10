import sys
import sqlite3 as sql


class FamilyClass:
    """Class for managing families"""
    def __init__(self, file):
        self.members = []
        self.fam_id = None

    def add_member(self, member):
        """Adds a member to the family"""
        self.fam_id = member['fam']
        self.members.append(member.copy())

    def clear(self):
        """Resets the class variables"""
        self.members = []
        self.fam_id = None
    def get_members(self):
        """Returns a list of members"""
        return self.members

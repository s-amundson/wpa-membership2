import sys
import sqlite3 as sql


class FamilyClass:
    def __init__(self, file):
        self.con = sql.connect(file)
        self.con.row_factory = sql.Row
        self.cur = self.con.cursor()
        self.members = []
        self.fam_id = None
    # def add_family(self, fam_id, mem_id):
    #     self.fam_id = self.execute("SELECT MAX(fam_id) as fid from family")[0]["fid"] + 1
    #     return self.fam_id
    def add_member(self, member):
        # if(self.fam_id == None):
        #     self.fam_id = self.execute("SELECT MAX(fam_id) as fid from family")[0]["fid"] + 1
        self.fam_id = member['fam']
        self.members.append(member.copy())
        # self.cur.execute("INSERT into family (fam_id, mem_id) values (?,?)", (self.fam_id, member["mem_id"]))
    def clear(self):
        self.members = []
        self.fam_id = None
    def get_members(self):
        return self.members
    def execute(self, statement, args=None):
        # try:
        if(args == None):
            self.cur.execute(statement)
        else:
            self.cur.execute(statement, args)
        self.con.commit()

        return self.cur.fetchall()
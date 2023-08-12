import sqlite3

class Database:
    
    def __init__(self, table="table.db") :
        self.con = sqlite3.connect(table, check_same_thread=False)
        self.cur = self.con.cursor()
        self.create_db()

    def create_db(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS task(do TEXT, status TEXT, date DATE)")
        self.con.commit()
        
    def add_db(self, do, status, date):
        data = (do, status, date)
        self.cur.execute("INSERT INTO task(do, status, date) VALUES(? ,? ,?)",data)
        self.con.commit()
        
    def read_db(self):
        self.cur.execute("SELECT * FROM task")
        return self.cur.fetchall()

    def view_task_names(self):
        self.cur.execute("SELECT DISTINCT do FROM task")
        return self.cur.fetchall()

    def get_task(self, do):
        self.cur.execute('SELECT * FROM task WHERE do="{}"'.format(do))
        return self.cur.fetchall()

    def get_task_statue(self,statue):
        self.cur.execute('SELECT *  FROM task WHERE do="{}"'.format(statue))
        return self.cur.fetchall()

    def edit_task_db(self, n_do,n_status,n_date,do,status,date):
        self.cur.execute("UPDATE task SET do=?,status=?, date=? WHERE do=? and status=? and date=?",
                    n_do,n_status,n_date,do,status,date)
        self.con.commit()
        return self.cur.fetchall()

    def delete_db(self, do):
        self.cur.execute('DELETE FROM task WHERE do="{}"'.format(do))
        self.con.commit()
    
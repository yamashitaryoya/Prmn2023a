import sqlite3

class Database:
    
    def __init__(self, table="table.db") :
        self.con = sqlite3.connect(table, check_same_thread=False)
        self.cur = self.con.cursor()
        self.create_db()

    def create_db(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS task(do TEXT, status TEXT, date DATE, priority TEXT)")
        self.con.commit()
        
    def add_db(self, do, status, date, priority):
        data = (do, status, date, priority)
        self.cur.execute("INSERT INTO task(do, status, date, priority) VALUES(? ,? ,?, ?)",data)
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

    def get_task_status(self, status):
        self.cur.execute('SELECT * FROM task WHERE status="{}"'.format(status))
        return self.cur.fetchall()
    
    def get_task_priority(self, priority):
        self.cur.execute('SELECT * FROM task WHERE priority="{}"'.format(priority))
        return self.cur.fetchall()
    
    def get_task_date(self):
        self.cur.execute('SELECT * FROM task ORDER BY Date ASC')
        return self.cur.fetchall()

    def edit_task_db(self, n_do, n_status, n_date, n_priority, do, status, date, priority):
        self.cur.execute("UPDATE task SET do=?, status=?, date=?, priority=? WHERE do=? and status=? and date=? and priority=?",
                    (n_do, n_status, n_date, n_priority, do, status, date, priority))
        self.con.commit()
        return self.cur.fetchall()

    def delete_db(self, do):
        self.cur.execute('DELETE FROM task WHERE do="{}"'.format(do))
        self.con.commit()
    
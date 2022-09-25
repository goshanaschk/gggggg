import sqlite3 as sq


class Database():
    def __init__(self, db_file):
        self.connect = sq.connect(db_file)
        self.cursor = self.connect.cursor()
        print('connected!')

    def add_new_relations(self, user_id, refer_id, use):
        with self.connect:
            self.cursor.execute("INSERT INTO users (user_id, referer) VALUES (?,?)",
                                (user_id, refer_id))

    def get_admins_id(self):
        with self.connect:
            all = self.cursor.execute("SELECT user_id FROM admins").fetchall()
            lst = [x for t in all for x in t]
            return lst

    def put_admin_id(self, user_id):
        with self.connect:
            self.cursor.execute("INSERT INTO admins (user_id) VALUES (?)",
                                (user_id,))

    def get_last_pid(self):
        with self.connect:
            all = self.cursor.execute("SELECT pid FROM pids").fetchall()
            lst = [x for t in all for x in t]
            return lst[0]

    def put_pid(self, pid):
        with self.connect:
            self.cursor.execute(f"""DELETE FROM pids WHERE status = 0""")
            self.cursor.execute("INSERT INTO pids (pid) VALUES (?)",
                                (pid,))

    def delete_admin(self, user_id):
        with self.connect:
            self.cursor.execute(f"""DELETE FROM admins WHERE user_id = {user_id}""")
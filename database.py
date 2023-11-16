import sqlite3

class Database(object):
    _instance = None

    """Return a singleton instance"""
    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    """Return a sqlite connection"""
    def __get_db_connection(self):
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        return conn

    def get_all_sharks(self):
        conn = self.__get_db_connection()
        sharks = conn.execute('SELECT * FROM sharks').fetchall()
        conn.close()
        return sharks

    def get_n_sharks(self, n):
        conn = self.__get_db_connection()
        # idx 0: name, 1: image
        sharks = conn.execute('SELECT name, image, bio FROM sharks where bio not null LIMIT ?', (n,)).fetchall()
        conn.close()
        return sharks

    def get_shark(self, shark_id):
        conn = self.__get_db_connection()
        shark = conn.execute('SELECT * FROM sharks WHERE id = ?',
                            (shark_id,)).fetchone()
        conn.close()
        if shark is None:
            print('No Sharks Here.')
        return shark


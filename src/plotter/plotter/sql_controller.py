import sqlite3
import pandas as pd

class SQLController():
    
    def __init__(self):
        self.__client = sqlite3.connect('src/plotter/plotter/db/db.db')

    def push(self, query):
        """
        Runs an insert query on the database.
        Used for adding new entries to the database.
        """
        cursor = self.__client.cursor()
        cursor.execute(query)
        self.__client.commit()
        cursor.close()
        return

    def pull(self, query) -> pd.DataFrame:
        cursor = self.__client.cursor()
        cur = cursor.execute(query)
        return pd.DataFrame(cur.fetchall())
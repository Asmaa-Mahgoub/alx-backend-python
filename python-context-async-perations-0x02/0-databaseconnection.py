import sqlite3
class DatabaseConnection:
    def __enter__(self):
        
        self.conn=sqlite3.connect("users.db")
        print("Database connection opened.")
        # Return the connection so it can be used inside the 'with' block
        return self.conn

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
        # Return False so any exceptions are not suppressed
        return False

with DatabaseConnection() as conn:
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM users")
    results=cursor.fetchall
    print("Query results:", results)

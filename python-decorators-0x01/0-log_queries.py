import sqlite3
import functools

#### decorator to log SQL queries
def log_queries(func):
    def wrapper(query):
        result = func(query)
        return result
        func(query)
    return wrapper
""" YOUR CODE GOES HERE"""

@log_queries
def fetch_all_users(query):
    conn=sqlite3.connect('users.db')
    cursor=conn.cursor()
    cursor.execute(query)
    results=cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
 
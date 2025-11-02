#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that fetches users from 'user_data' table in batches.
    Yields a list (batch) of user dictionaries each time.
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",             # <-- replace with your MySQL username
        password="yourpassword", # <-- replace with your MySQL password
        database="your_database" # <-- replace with your database name
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        # Fetch a batch of rows
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    conn.close()


def batch_processing(batch_size):
    """
    Processes user batches and prints users over age 25.
    Uses generator from stream_users_in_batches().
    """
    for batch in stream_users_in_batches(batch_size):       # loop 1
        for user in batch:                                  # loop 2
            if user["age"] > 25:
                print(user)

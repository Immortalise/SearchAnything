import sqlite3  
import numpy as np
import os

from config import DB_PATH

import sqlite3   


def init_db():
    conn = sqlite3.connect(DB_PATH)

    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS file_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        page INTEGER,
        file_path TEXT,
        subject TEXT,
        content TEXT,
        embedding BLOB
    )
    ''')
    conn.commit()

    return conn


def insert_data(conn, line_list):
    c = conn.cursor()

    for line in line_list:
        
        line['embedding'] = line['embedding'].tobytes()

        columns = ', '.join(line.keys())
        placeholders = ', '.join(['?' for _ in line])
        values = tuple(line.values())
    
        query = f'INSERT INTO file_data ({columns}) VALUES ({placeholders})'

        c.execute(query, values)
    
        conn.commit()  
 
  
def get_file_paths(conn):  
    # Connect to the SQLite database  
    c = conn.cursor()  
  
    # Fetch all file paths from the table  
    c.execute('SELECT file_path FROM file_data')  
    file_paths = c.fetchall()  
  
    file_path_set = set(file_path[0] for file_path in file_paths)  
  
    return file_path_set   


def retrieve_data(conn, indices):
    indices = indices.tolist()[0]
    print(type(indices))

    c = conn.cursor()
    placeholders = ','.join('?' * len(indices))
    query = f'SELECT * FROM file_data WHERE id IN ({placeholders})'
    c.execute(query, tuple(indices))
    rows = c.fetchall()
    column_names = [desc[0] for desc in c.description]
    print(column_names)

    for i, row in enumerate(rows):
        print(f"Result {i+1}:")

        for name, value in zip(column_names, row):
            if name in ['title', 'file_path', 'page', 'author', 'subject']:
                print(f"{name}: {value}")   
            if name in ['content']:
                print(f"{name}: {value[:100]}...")
        
        print('\n')

import sqlite3  
import numpy as np
import os

from config import DB_PATH

import sqlite3   


def init_db():
    conn = sqlite3.connect(DB_PATH)

    if not os.path.exists(DB_PATH): 
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS file_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            embedding BLOB
        )
        ''')
        conn.commit()

    return conn


def insert_data(conn, data):
    c = conn.cursor()

    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?' for _ in data])
    values = tuple(data.values())
  
    query = f'INSERT INTO example_data ({columns}) VALUES ({placeholders})'
    c.execute(query, values)
  
    conn.commit()  


def retrieve_data(conn, indices, distances, k=5):
    c = conn.cursor()  
    
    # Iterate over the indices of the top k most similar embeddings  
    for i in range(k):  
        index = indices[0][i]  
        distance = distances[0][i]  
    
        # Retrieve the corresponding file data from the database  
        c.execute('SELECT * FROM file_data WHERE id=?', (index + 1,))  
        row = c.fetchone()  
    
        if row is not None:  
            file = {  
                'id': row[0],  
                'title': row[1],  
                'content': row[2],  
                'embedding': np.frombuffer(row[3], dtype=np.float32)  
            }  
    
            print(f"Rank: {i + 1}")  
            print(f"Title: {file['title']}")  
            print(f"Content: {file['content']}")  
            print(f"Distance: {distance}\n")  
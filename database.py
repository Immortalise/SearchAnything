import sqlite3  
import numpy as np
import os

from config import DB_PATH

import sqlite3


class DataBase(object):
    def __init__(self) -> None:

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
        conn.close()


    def insert_data(self, line_list):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        inserted_ids = []

        for line in line_list:
            
            line['embedding'] = line['embedding'].tobytes()

            columns = ', '.join(line.keys())
            placeholders = ', '.join(['?' for _ in line])
            values = tuple(line.values())
        
            query = f'INSERT INTO file_data ({columns}) VALUES ({placeholders})'

            c.execute(query, values)
        
            conn.commit()

            last_inserted_id = c.lastrowid  
            inserted_ids.append(last_inserted_id)

            line['embedding'] = np.frombuffer(line['embedding'], dtype=np.float32)

            conn.close()

        return inserted_ids


    def delete_data(self, path, is_directory=False):  
        # Get the cursor object to execute SQL queries
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
    
        if is_directory:
            # Make sure the path ends with a path separator
            if not path.endswith('/'):
                path = path + '/'
            query = f'DELETE FROM file_data WHERE file_path LIKE ?'
            match_value = path + '%'
        else:
            query = f'DELETE FROM file_data WHERE file_path=?'
            match_value = path
    
        # Execute the query and delete rows with a matching path or directory prefix
        c.execute(query, (match_value,))
        
        # Commit the transaction to the database
        conn.commit()
    
        # Retrieve the remaining data embeddings and IDs
        c.execute('SELECT id, embedding FROM file_data')
        remaining_data = c.fetchall()
    
        # Extract the remaining embeddings and IDs
        remaining_ids = [row[0] for row in remaining_data]
        remaining_embeddings = [np.frombuffer(row[1], dtype=np.float32) for row in remaining_data]
        conn.close()
    
        return remaining_embeddings, remaining_ids  

  
    def get_existing_file_paths(self):  
        # Connect to the SQLite database
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
    
        # Fetch all file paths from the table  
        c.execute('SELECT file_path FROM file_data')  
        file_paths = c.fetchall()  
    
        file_path_set = set(file_path[0] for file_path in file_paths)
        conn.close() 
    
        return file_path_set   


    def retrieve_data(self, indices):
        indices = indices.tolist()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        placeholders = ','.join('?' * len(indices))
        query = f'SELECT * FROM file_data WHERE id IN ({placeholders})'
        c.execute(query, tuple(indices))
        rows = c.fetchall()
        column_names = [desc[0] for desc in c.description]
        # print(column_names)

        # for i, row in enumerate(rows):
        #     print(f"Result {i+1}:")

        #     for name, value in zip(column_names, row):
        #         if name in ['title', 'file_path', 'page', 'author', 'subject', 'content']:
        #             print(f"{name}: {value}")
            
        #     print('\n')
        conn.close()

        return column_names, rows

    def retrieve_data_custom_query(self, query):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(query)
        rows = c.fetchall()
        column_names = [desc[0] for desc in c.description]
        conn.close()
        return column_names, rows

    def close(self):
        pass

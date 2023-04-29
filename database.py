import sqlite3  
import numpy as np
import os

from config import DB_PATH

import sqlite3


class DataBase(object):
    def __init__(self) -> None:

        self.conn = sqlite3.connect(DB_PATH)

        self.c = self.conn.cursor()
        self.c.execute('''
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
        self.conn.commit()


    def insert_data(self, line_list):
        c = self.conn.cursor()

        inserted_ids = []

        for line in line_list:
            
            line['embedding'] = line['embedding'].tobytes()

            columns = ', '.join(line.keys())
            placeholders = ', '.join(['?' for _ in line])
            values = tuple(line.values())
        
            query = f'INSERT INTO file_data ({columns}) VALUES ({placeholders})'

            c.execute(query, values)
        
            self.conn.commit()

            last_inserted_id = c.lastrowid  
            inserted_ids.append(last_inserted_id)

            line['embedding'] = np.frombuffer(line['embedding'], dtype=np.float32)

        return inserted_ids


    def delete_data(self, path, is_directory=False):    
        # Get the cursor object to execute SQL queries    
        c = self.conn.cursor()    
    
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
        self.conn.commit()  
    
        # Retrieve the remaining data embeddings and IDs  
        c.execute('SELECT id, embedding FROM file_data')  
        remaining_data = c.fetchall()  
    
        # Extract the remaining embeddings and IDs  
        remaining_ids = [row[0] for row in remaining_data]  
        remaining_embeddings = [np.frombuffer(row[1], dtype=np.float32) for row in remaining_data]  
    
        return remaining_embeddings, remaining_ids  

  
    def get_existing_file_paths(self):  
        # Connect to the SQLite database  
        c = self.conn.cursor()  
    
        # Fetch all file paths from the table  
        c.execute('SELECT file_path FROM file_data')  
        file_paths = c.fetchall()  
    
        file_path_set = set(file_path[0] for file_path in file_paths)  
    
        return file_path_set   


    def retrieve_data(self, indices):
        indices = indices.tolist()

        c = self.conn.cursor()
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

        return column_names, rows

    def close(self):
        self.conn.close()


import unittest  
import numpy as np  
  
class TestDatabaseClass(unittest.TestCase):  
  
    def test_database_operations(self):  
        # Initialize the database and create a test table  
        db = DataBase()  
  
        # Insert data into the database  
        line_list = [  
            {  
                'title': 'Test Title 1',  
                'author': 'Test Author 1',  
                'page': 1,  
                'file_path': '/test/path1',  
                'subject': 'Test Subject 1',  
                'content': 'Test content 1',  
                'embedding': np.random.random(1024).astype('float32')  
            },  
            {  
                'title': 'Test Title 2',  
                'author': 'Test Author 2',  
                'page': 2,  
                'file_path': '/test/path2',  
                'subject': 'Test Subject 2',  
                'content': 'Test content 2',  
                'embedding': np.random.random(1024).astype('float32')  
            },  
        ]  
        inserted_ids = db.insert_data(line_list)  
        self.assertEqual(len(inserted_ids), 2)  
  
        # Delete data from the database  
        remaining_embeddings, remaining_ids = db.delete_data('/test/', is_directory=True)  
  
  
if __name__ == "__main__":  
    unittest.main()  
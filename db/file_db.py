import sqlite3  
import numpy as np

from .base_db import Base_DB


class File_DB(Base_DB):
    def __init__(self) -> None:

        sql = '''
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
        '''
        super().__init__(sql)



    def insert_data(self, line_list):
        conn = sqlite3.connect(self.db_path)
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
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
    
        if is_directory:
            if not path.endswith('/'):
                path = path + '/'
            query = f'DELETE FROM file_data WHERE file_path LIKE ?'
            match_value = path + '%'
        else:
            query = f'DELETE FROM file_data WHERE file_path=?'
            match_value = path
    
        c.execute(query, (match_value,))
        
        conn.commit()
    
        c.execute('SELECT id, embedding FROM file_data')
        remaining_data = c.fetchall()
    
        remaining_ids = [row[0] for row in remaining_data]
        remaining_embeddings = [np.frombuffer(row[1], dtype=np.float32) for row in remaining_data]
        conn.close()
    
        return remaining_embeddings, remaining_ids  



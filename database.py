import sqlite3
import numpy as np
from config import DB_PATH, DATA_TYPES


class Base_DB(object):

    def __init__(self, sql) -> None:
        self.db_path = DB_PATH
        conn = sqlite3.connect(DB_PATH)

        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()

    def insert_data(self, data_list, data_type):
        
        if data_list is None:
            return

        assert data_type in DATA_TYPES

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        inserted_ids = []

        for data in data_list:
            
            data['embedding'] = data['embedding'].tobytes()

            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            values = tuple(data.values())
        
            query = f'INSERT INTO {data_type}_data ({columns}) VALUES ({placeholders})'

            c.execute(query, values)
        
            conn.commit()

            last_inserted_id = c.lastrowid  
            inserted_ids.append(last_inserted_id)

            data['embedding'] = np.frombuffer(data['embedding'], dtype=np.float32)

        conn.close()


    def delete_data(self, path, data_type, is_directory=False):
        assert data_type in DATA_TYPES

        conn = sqlite3.connect(self.db_path)
        
        c = conn.cursor()
    
        if is_directory:
            if not path.endswith('/'):
                path = path + '/'
            query = f'DELETE FROM {data_type}_data WHERE file_path LIKE ?'
            match_value = path + '%'
        else:
            query = f'DELETE FROM {data_type}_data WHERE file_path=?'
            match_value = path
    
        c.execute(query, (match_value,))
        
        conn.commit()
    
        c.execute(f'SELECT id, embedding FROM {data_type}_data')
        remaining_data = c.fetchall()
    
        remaining_ids = [row[0] for row in remaining_data]
        remaining_embeddings = [np.frombuffer(row[1], dtype=np.float32) for row in remaining_data]
        conn.close()
    
        return remaining_embeddings, remaining_ids  

    def get_existing_file_paths(self, data_type):
        
        assert data_type in DATA_TYPES

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
    
        c.execute(f'SELECT file_path FROM {data_type}_data')
        file_paths = c.fetchall()
    
        file_path_set = set(file_path[0] for file_path in file_paths)
        conn.close()
    
        return file_path_set   

    def retrieve_data(self, data_type, indices=None, query=None):
        
        assert data_type in DATA_TYPES

        conn = sqlite3.connect(self.db_path)  
        c = conn.cursor()  
  
        if query:  
            c.execute(query)  
        else:  
            indices = indices.tolist()  
            placeholders = ','.join('?' * len(indices))  
            query = f'SELECT * FROM {data_type}_data WHERE id IN ({placeholders})'  
            c.execute(query, tuple(indices))  
  
        rows = c.fetchall()  
        column_names = [desc[0] for desc in c.description]  
  
        conn.close()  
  
        return column_names, rows  

    def close(self):
        pass


class Text_DB(Base_DB):
    def __init__(self) -> None:

        sql = '''
        CREATE TABLE IF NOT EXISTS text_data (
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


class Image_DB(Base_DB):
    def __init__(self) -> None:
        sql = '''
        CREATE TABLE IF NOT EXISTS image_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT,
            content TEXT,
            embedding BLOB
        )
        '''

        super().__init__(sql)

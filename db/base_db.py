import sqlite3  

from config import DB_PATH



class Base_DB(object):
    def __init__(self, sql) -> None:
        self.db_path = DB_PATH
        conn = sqlite3.connect(DB_PATH)

        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()


    def insert_data(self, *args):
        raise NotImplementedError


    def delete_data(self, *args):
        raise NotImplementedError

  
    def get_existing_file_paths(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
    
        c.execute('SELECT file_path FROM file_data')  
        file_paths = c.fetchall()  
    
        file_path_set = set(file_path[0] for file_path in file_paths)
        conn.close() 
    
        return file_path_set   


    def retrieve_data(self, indices=None, query=None):  
        conn = sqlite3.connect(self.db_path)  
        c = conn.cursor()  
  
        if query:  
            c.execute(query)  
        else:  
            indices = indices.tolist()  
            placeholders = ','.join('?' * len(indices))  
            query = f'SELECT * FROM file_data WHERE id IN ({placeholders})'  
            c.execute(query, tuple(indices))  
  
        rows = c.fetchall()  
        column_names = [desc[0] for desc in c.description]  
  
        conn.close()  
  
        return column_names, rows  


    def close(self):
        pass

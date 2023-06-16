from .base_db import Base_DB


class Image_DB(Base_DB):
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
    
    def insert_data(self, *args):
        return super().insert_data(*args)
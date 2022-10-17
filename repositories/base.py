from databases import Database

class BaseRepository:
    """
    Это родительский класс для всех остальных репозиториев
    """
    def __init__(self, database: Database):
        self.database = database


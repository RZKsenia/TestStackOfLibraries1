"""
Здесь хранятся зависимости.
"""
from repositories.users import UserRepository as user_repository
from db.base import database

def get_user_repository() -> user_repository:
    return user_repository(database)
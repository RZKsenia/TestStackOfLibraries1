from typing import List, Optional
from db.users import users
from repositories.base import BaseRepository
from models.user import User, UserIn
import datetime
from core.sequrity import hash_password


class UserRepository(BaseRepository):
    """
    -> Type - указывает тип возвращаемого фукнцией значения
    """

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[User]:
        """
        :param limit: максимальное количество пользователей, которое можем получить
        :param skip: сколько пользователей пропустить для реализации пагинации (способ возвращать
        объекты постранично).
        :return:
        """
        query = users.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def get_by_id(self, id: int) -> Optional[User]:
        """
        Получить пользователя по его id
        :param id: идентификатор пользователя в табилце users
        :return:
        """
        query = users.select().where(users.c.id == id).first()
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)  # превращаем объект БД в объект User

    async def create(self, u: UserIn) -> User:
        """
        Создание пользователя
        :return:
        """
        new_user = User(
            name=u.name,
            email=u.email,
            hashed_password=hash_password(u.password),
            is_company=u.is_company,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        values = {**new_user.dict()}
        values.pop('id', None)  # это поле не нужно добавлять в таблицу, поэтому удаляем его.

        query = users.insert(values)
        new_user.id = await self.database.execute(query)

        return new_user

    async def update(self, id: int, u: UserIn) -> User:
        """
        Обновление данных о пользователе
        :param id: id пользователя в БД
        :param u: пользователь, как экземпляр UserIn
        :return:
        """
        updated_user = User(
            id=id,
            name=u.name,
            email=u.email,
            hashed_password=hash_password(u.password),
            is_company=u.is_company,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        values = {**updated_user.dict()}
        values.pop('id', None)  # это поле не нужно добавлять в таблицу, поэтому удаляем его.
        values.pop('created_at', None)  # это поле не нужно обновлять, т.к. пользователь в БД уже существует.

        query = users.update().where(users.c.id == id).values(**values)
        await self.database.execute(query)
        return updated_user

    async def get_by_email(self, email: str) -> User:
        """
        Получить пользователя по адресу электронной почты
        :param email: тип str
        :return:
        """
        query = users.select().where(users.c.email == email).first()
        user = await self.database.fetch_one(query)
        if user is None:
            return None
        return User.parse_obj(user)  # превращаем объект БД в объект User

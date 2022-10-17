"""
Здесь хранятся зависимости.
Внедрение зависимостей - это концепция в программировании, когда объект получает другие объекты,
от которых он зависит. Остальные объекты называются зависимостями. Это сводит к минимуму повторение
кода и упрощает тестирование ваших систем.
Согласно официальной документации, внедрение зависимостей дает возможность:
    - повторно использовать ту же общую логику
    - совместно использовать подключения к базе данных
    - применять функции аутентификации и безопасности
    - и многое другое

"""
from repositories.users import UserRepository as user_repository
from repositories.jobs import JobRepository as job_repository
from db.base import database
from models.user import User
from fastapi import Depends, HTTPException, status
from core.sequrity import JWTBearer, decode_access_token


def get_user_repository() -> user_repository:
    return user_repository(database)


async def get_current_user(user_rep: user_repository = Depends(get_user_repository),
                           token: str = Depends(JWTBearer())) -> User:
    exception_for_return = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                         detail='Неверные данные пользователя или пользователь не существует.')
    decoded_token = decode_access_token(token)
    if decoded_token is None:
        raise exception_for_return

    email: str = decoded_token.get('sub')
    if email is None:
        raise exception_for_return

    user = await user_rep.get_by_email(email=email)
    if user is None:
        raise exception_for_return

    return user


def get_job_repository() -> job_repository:
    return job_repository(database)
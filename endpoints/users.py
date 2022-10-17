from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from repositories.users import UserRepository
from endpoints.depends import get_user_repository, get_current_user
from models.user import User, UserIn

router = APIRouter()


@router.get('/', response_model=List[User])
async def read_users(user_repository: UserRepository = Depends(get_user_repository), limit: int = 100, skip: int = 100):
    """
    Получение всех пользователей
    :param user_repository: репозиторий User
    :param limit: максимальное количество пользователей, которое можем получить
    :param skip: сколько пользователей пропустить для реализации пагинации (способ возвращать
    :return: список пользователей
    """
    return await user_repository.get_all(limit=limit, skip=skip)


@router.post('/', response_model=User)
async def create_user(user_data: UserIn, user_repository: UserRepository = Depends(get_user_repository)):
    """
    Создание пользователя
    :param user_data: данные, полученные от пользователя в запросе
    :param user_repository: репозиторий пользователя - User
    :return: 
    """
    result = await user_repository.create(u=user_data)
    result.hashed_password = ''
    return result

@router.put('/', response_model=User)
async def update_user(id_of_user: int,
                      user_data: UserIn,
                      user_repository: UserRepository = Depends(get_user_repository),
                      current_user: User = Depends(get_current_user)):
    """
    Обноваление пользователя
    :param id_of_user: id пользователя, чьи данные будем обновлять
    :param user_data: данные пользователя
    :param user_repository: репозиторий пользователя
    :return:
    """
    old_user = await user_repository.get_by_id(id=id_of_user)
    if old_user is None or old_user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден.')
    return await user_repository.update(id=id_of_user, u=user_data)

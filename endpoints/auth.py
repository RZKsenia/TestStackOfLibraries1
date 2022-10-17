"""
Аутентификация пользователя
"""
from fastapi import APIRouter, Depends, HTTPException, status
from models.token import Token, Login
from repositories.users import UserRepository
from endpoints.depends import get_user_repository
from core.sequrity import verify_password, create_access_token

router = APIRouter()


@router.post('/', response_model=Token)
async def login(login: Login, user_repository: UserRepository = Depends(get_user_repository)):
    """
    Логирование пользователя
    :return:
    """
    auth_user = await user_repository.get_by_email(login.email)
    if auth_user is None or not verify_password(login.password, auth_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Неверный логин или пароль')
    return Token(access_string=create_access_token({'sub':login.email}),
                 token_type='Bearer')
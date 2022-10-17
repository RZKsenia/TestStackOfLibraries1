"""
В этом файле собраны все функции, связанные с безопасностью приложения.
"""
from passlib.context import CryptContext
from jose import jwt
import datetime
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, status

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    """
    хэширование паролей
    :param password: пароль для хэширования
    :return: хэшированный пароль
    """
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    """
    сверка паролей пользователя
    :param password: пароль для проверки
    :param hash: хэшированный пароль
    :return:
    """
    return pwd_context.verify(password, hash)


def create_access_token(data_from_user: dict) -> str:
    """
    формирование токена доступа
    :param data_from_user: данные для подписания токеном
    :return:
    """
    data_to_encode = data_from_user.copy()
    data_to_encode.update({'ext': str(datetime.datetime.utcnow() + datetime.timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)))})

    return jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    """
    Расшифровка токена
    :param token: строка
    :return:
    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except jwt.JWTError:
        return None
    return decoded_token


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        exception_for_return = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                 detail='Неверный токен авторизации')

        if credentials:
            token = decode_access_token(credentials.credentials)
            if token is None:
                raise exception_for_return
            return credentials.credentials
        else:
            raise exception_for_return
import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr

class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    hashed_password: str
    is_company: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

class UserIn(BaseModel):
    """
    Присылаемые пользователем данные
    """
    name: str
    email: EmailStr
    password: constr(min_lenght=8)
    password2: str  # это подтверждение пароля
    is_company: bool = False # признак - регистрируется компания или обычный пользователь

    @validator('password2')
    def password_match(self, v, values, *kwargs):
        """
        Сверка присланных паролей
        :param v: значение поля password2
        :param values: все значения, которые есть в нашей модели, которые пользователь присылал
        :param kwargs:
        :return:
        """
        if 'password' in values and v != values['password']:
            raise ValueError('Пароли не совпадают')
        return v
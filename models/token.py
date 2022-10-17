from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_string: str
    token_type: str


class Login(BaseModel):
    """
    Это данные, которые будет присылать пользователь чтобы
    залогиниться в приложение.
    """
    email: EmailStr
    password: str
    
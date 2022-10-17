from pydantic import BaseModel
import datetime


class BaseJobInfo(BaseModel):
    title: str
    description: str
    salary_from: int
    salary_to: int
    is_active: bool = True


class Job(BaseJobInfo):
    id: int
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

class JobIn(BaseJobInfo):
    """
    Класс для данных, которые будет присылать нам пользователь
    """
    pass


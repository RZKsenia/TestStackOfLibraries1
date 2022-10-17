from typing import List, Optional
from db.jobs import jobs
from repositories.base import BaseRepository
from models.jobs import Job, JobIn
import datetime
from core.sequrity import hash_password


class JobRepository(BaseRepository):
    def create(self, user_id: int, new_job: JobIn) -> Job:
        """
        Создание нового объявления о работе
        :param user_id: идентификатор пользователя, создающего объявление
        :param new_job: содержание объявления
        :return:
        """
        # создаём экземпляр модели
        job = Job(
            user_id = user_id,
            title=new_job.title,
            description=new_job.description,
            salary_from=new_job.salary_from,
            salary_to=new_job.salary_to,
            is_active=new_job.is_active,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        values = {**job.dict()}
        values.pop('id', None)
        query = jobs.insert().values(**values)
        job.id = self.database.execute(query)
        return job

    def update(self, job_id: int, user_id: int, new_job_info: JobIn) -> Job:
        """
        Обновление объявления о работе
        :param job_id: идентификатор объявления о работе
        :param user_id: идентификатор поль
        :param new_job:
        :return:
        """
        job = Job(
            user_id=user_id,
            title=new_job_info.title,
            description=new_job_info.description,
            salary_from=new_job_info.salary_from,
            salary_to=new_job_info.salary_to,
            is_active=new_job_info.is_active,
            updated_at=datetime.datetime.utcnow()
        )
        values = {**job.dict()}
        values.pop('id', None)
        values.pop('created_at', None)
        query = jobs.update().where(jobs.c.id == job_id).values(**values)
        self.database.execute(query)
        return job

    def get_list(self, limit: int = 100, skip: int = 0) -> List[Job]:
        """
        Получить список объявлени о работе
        :param limit: максимальное количество пользователей, которое можем получить
        :param skip: сколько пользователей пропустить для реализации пагинации (способ возвращать
        объекты постранично).
        :return: список объявлений о работе
        """
        query = jobs.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    def delete(self, job_id: int):
        query = jobs.delete().where(jobs.c.id == job_id)
        return await self.database.execute(query)
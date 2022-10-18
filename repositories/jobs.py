from typing import List, Optional
from db.jobs import jobs
from repositories.base import BaseRepository
from models.jobs import Job, JobIn
import datetime


class JobRepository(BaseRepository):
    async def create(self, user_id: int, new_job: JobIn) -> Job:
        """
        Создание нового объявления о работе
        :param user_id: идентификатор пользователя, создающего объявление
        :param new_job: содержание объявления
        :return:
        """
        # создаём экземпляр модели
        job = Job(
            id=0,
            user_id=user_id,
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
        job.id = await self.database.execute(query)
        return job

    async def update(self, job_id: int, user_id: int, new_job_info: JobIn) -> Job:
        """
        Обновление объявления о работе
        :param job_id: идентификатор объявления о работе
        :param user_id: идентификатор поль
        :param new_job:
        :return:
        """
        updated_job = Job(
            id=job_id,
            user_id=user_id,
            title=new_job_info.title,
            description=new_job_info.description,
            salary_from=new_job_info.salary_from,
            salary_to=new_job_info.salary_to,
            is_active=new_job_info.is_active,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        values = {**updated_job.dict()}
        values.pop('id', None)
        values.pop('created_at', None)
        query = jobs.update().where(jobs.c.id == job_id).values(**values)
        await self.database.execute(query)
        return updated_job

    async def get_list(self, limit: int = 100, skip: int = 0) -> List[Job]:
        """
        Получить список объявлени о работе
        :param limit: максимальное количество пользователей, которое можем получить
        :param skip: сколько пользователей пропустить для реализации пагинации (способ возвращать
        объекты постранично).
        :return: список объявлений о работе
        """
        query = jobs.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def delete(self, job_id: int):
        """
        Удалить объявление о работе
        :param job_id: идентификатор объявления о работе
        :return:
        """
        query = jobs.delete().where(jobs.c.id == job_id)
        return await self.database.execute(query)

    async def get_by_id(self, job_id: int) -> Optional[Job]:
        """
        Получить объявление о работе по его id
        :param job_id: идентификатор обэявление о работе
        :return: объявление о работе (Job)
        """
        query = jobs.select().where(jobs.c.id == job_id)
        job = await self.database.fetch_one(query)
        if job is None:
            return None
        return Job.parse_obj(job)

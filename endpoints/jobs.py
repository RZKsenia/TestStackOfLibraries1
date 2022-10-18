from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from repositories.jobs import JobRepository
from endpoints.depends import get_job_repository, get_current_user
from models.jobs import Job, JobIn
from models.user import User

router = APIRouter()

@router.get('/', response_model=List[Job])
async def read_jobs(limit: int = 100,
                    skip: int = 0,
                    jobs_rep: JobRepository = Depends(get_job_repository)) -> List[Job]:
    """Получить список объявлени о работе
        :param jobs_rep: репозиторий объявления о работе
        :param limit: максимальное количество пользователей, которое можем получить
        :param skip: сколько пользователей пропустить для реализации пагинации (способ возвращать
        объекты постранично).
        :return: список объявлений о работе"""
    return await jobs_rep.get_list(limit=limit, skip=skip)


@router.post('/', response_model=Job)
async def create_jobs(new_job: JobIn,
                      jobs_rep: JobRepository = Depends(get_job_repository),
                      current_user: User = Depends(get_current_user)) -> Job:
    """
    Создание нового объявления о работе
    :param current_user: идентификатор текущего пользователя, создающего объявление
    :param new_job: содержание объявления
    :param jobs_rep: репозиторий объявления о работе
    :return:
    """
    return await jobs_rep.create(user_id=current_user.id, new_job=new_job)


@router.put('/', response_model=Job)
async def update_jobs(job_id: int,
                      new_job_info: JobIn,
                      jobs_rep: JobRepository = Depends(get_job_repository),
                      current_user: User = Depends(get_current_user)) -> Job:
    """
    Обновление объявления о работе
    :param job_id: идентификатор объявления о работе
    :param new_job_info: обновлённая информация для объявления о работе
    :param jobs_rep: репозиторий объявления о работе
    :param`current_user: идентификатор текущего пользователя, редактирующего объявление
    :return:
    """
    job_for_update = await jobs_rep.get_by_id(job_id=job_id)

    if job_for_update is None or job_for_update.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Объявление о работе не найдено.')
    return await jobs_rep.update(job_id=job_id, user_id=current_user.id, new_job_info=new_job_info)


@router.delete('/')
async def delete_jobs(job_id: int,
                      jobs_rep: JobRepository = Depends(get_job_repository),
                      current_user: User = Depends(get_current_user)):
    """
    Удалить объявление о работе
    :param job_id: идентификатор объявления о работе
    :return:
    """
    job_for_delete = await jobs_rep.get_by_id(job_id)
    exception_for_display = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                          detail='Объявление о работе не найдено.')

    if job_for_delete is None or job_for_delete.user_id != current_user.id:
        raise exception_for_display

    result = await jobs_rep.delete(job_id=job_id)

    return result

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from endpoints.users import router as users_router
from endpoints.jobs import router as jobs_router
from endpoints.auth import router as auth_router
import uvicorn

from db.base import database
from db.base import engine_sync

app = FastAPI(title='Employment exchange')
app.include_router(users_router, prefix='/users', tags=['users'])
app.include_router(jobs_router, prefix='/jobs', tags=['jobs'])
app.include_router(auth_router, prefix='/auth', tags=['auth'])


@app.on_event('startup')
async def startup():
    """
    Выполняется при запуске приложения
    :return:
    """
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    """
    Выполняется при закрытии приложения
    :return:
    """
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)

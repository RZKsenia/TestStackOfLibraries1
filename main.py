from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from db.base import database

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get('/')
def read_root():
    return {'Hello': 'World'}

@app.get('/items/{item_id}')
def read_item(item_id: int, q: Union[str, None] = None):
    return {'item_id': item_id, 'q': q}

@app.put('/items/{item_id}')
def update_item(item_id: int, item: Item):
    """
    Обработка запроса на обноваление предмета
    :param item_id:
    :param item:
    :return:
    """
    return {'item_name': item.name, 'item_id': item_id}


@app.on_event('startup')
async def startup():
    """
    Выполняется при запуске приложения
    :return:
    """
    database.connect()


@app.on_event('shutdown')
async def shutdown():
    """
    Выполняется при закрытии приложения
    :return:
    """
    database.disconnect()

if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)
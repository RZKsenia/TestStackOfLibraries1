from databases import Database
from sqlalchemy import create_engine, MetaData
from core.config import DATABASE_URL

metadata = MetaData()
database = Database(DATABASE_URL)
engine_sync = create_engine(DATABASE_URL)
metadata.create_all(engine_sync)






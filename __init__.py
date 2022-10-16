from .db.users import users
from .db.jobs import jobs
from .db.base import engine_sync, metadata

metadata.create_all(bind=engine_sync)

from starlette.config import Config

config = Config('.env')

#REALM_NAME = config('REALM_NAME')
#CLIENT_ID = config('CLIENT_ID')
#CLIENT_SECRET = config('CLIENT_SECRET')
#SERVER_URL = config('SERVER_URL')
#TOKEN_URL = config('TOKEN_URL')

PG_PASSWORD = config('PG_PASSWORD')
PG_USERNAME = config('PG_USERNAME')
PG_DATABASE = config('PG_DATABASE')
PG_HOST = config('PG_HOST')
PG_PORT = config('PG_PORT')

#DATABASE_URL = config('TESTSTACKOFLIBRARIES_DATABASE_URL',
#                      cast=str,
#                     default='')"""

DATABASE_URL = (
    f"postgresql+psycopg2://{PG_USERNAME}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
)

ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES")

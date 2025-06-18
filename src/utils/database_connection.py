from utils.database import DatabaseClient
from utils.config import (
    SHAREPOINT_POSTGRES_DB_HOST, SHAREPOINT_POSTGRES_DB_USER, SHAREPOINT_POSTGRES_DB_PASS,
    SHAREPOINT_POSTGRES_DB_DATABASE, SHAREPOINT_POSTGRES_DB_PORT
)


def get_sharepoint_db():
    return DatabaseClient(
        db_type='postgresql',
        database=SHAREPOINT_POSTGRES_DB_DATABASE,
        username=SHAREPOINT_POSTGRES_DB_USER,
        password=SHAREPOINT_POSTGRES_DB_PASS,
        host=SHAREPOINT_POSTGRES_DB_HOST,
        port=SHAREPOINT_POSTGRES_DB_PORT
    )

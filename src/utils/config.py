import os
from dotenv import load_dotenv


# loads .env file, will not overide already set enviroment variables (will do nothing when testing, building and deploying)
load_dotenv()


DEBUG = os.getenv('DEBUG', 'False') in ['True', 'true']
PORT = os.getenv('PORT', '8080')
POD_NAME = os.getenv('POD_NAME', 'pod_name_not_set')

# Postgres DB
SHAREPOINT_POSTGRES_DB_HOST = os.getenv("SHAREPOINT_POSTGRES_DB_HOST")
SHAREPOINT_POSTGRES_DB_USER = os.getenv("SHAREPOINT_POSTGRES_DB_USER")
SHAREPOINT_POSTGRES_DB_PASS = os.getenv("SHAREPOINT_POSTGRES_DB_PASS")
SHAREPOINT_POSTGRES_DB_DATABASE = os.getenv("SHAREPOINT_POSTGRES_DB_DATABASE")
SHAREPOINT_POSTGRES_DB_PORT = os.getenv("SHAREPOINT_POSTGRES_DB_PORT")

import os

from dotenv import load_dotenv

load_dotenv('.env')

DEFAULT_MAX_WORKERS = int(os.getenv('DEFAULT_MAX_WORKERS', 9))
ATHENA_THREADS_QUERY = int(os.getenv('ATHENA_THREADS_QUERY', 9))

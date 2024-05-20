from pathlib import Path
import os


LOG_DIR = Path(__file__).resolve().parent.joinpath('logs')

bind = '0.0.0.0:8000'
workers = int(os.getenv('GUNICORN_WORKERS_COUNT', os.cpu_count()))
proc_name = 'trainer_backend'

errorlog = f'{LOG_DIR}/gunicorn.log'
loglevel = 'error'
timeout = 660

from pathlib import Path
import os


LOG_DIR = Path(__file__).resolve().parent.parent.joinpath('logs')

bind = f'0.0.0.0:{os.getenv("BACKEND_PORT", 4000)}'

workers = int(os.getenv('GUNICORN_WORKERS_COUNT', os.cpu_count() + 1))
proc_name = 'trainer_backend'

errorlog = f'{LOG_DIR}/gunicorn.log'
loglevel = 'error'
timeout = 660

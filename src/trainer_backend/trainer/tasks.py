from trainer_backend.celery_config import celery_app

from .usecases import GenerateAnswerArchiveUseCase
from .usecases import ProcessAnswerUseCase


@celery_app.task
def process_answer_task(answer_id=None, **kwargs):
    """Задача на обработку ответа."""
    ProcessAnswerUseCase().execute(answer_id)
    GenerateAnswerArchiveUseCase().execute(answer_id)

from trainer_backend.celery_config import celery_app

from .usecases import GenerateAnswerArchive


@celery_app.task
def generate_answer_archive(*args, answer_id=None, **kwargs):
    """Задача на формирование архива ответа."""
    GenerateAnswerArchive().execute(answer_id)

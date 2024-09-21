from django.db.models import F

from trainer_backend.core.db.repositories import BaseModelRepository
from trainer_backend.trainer.models import Answer
from trainer_backend.trainer.models import Image
from trainer_backend.trainer.models import Question
from trainer_backend.trainer.models import QuestionAnswer
from trainer_backend.trainer.models import Task
from trainer_backend.trainer.models import TaskAnswer


class TaskRepository(BaseModelRepository):
    """Репозиторий для работы с заданиями."""

    _model = Task

    def get_tasks_by_answer(self, answer_id):
        """Получить информацию о заданиях в ответах."""
        return self._read(
            filters=dict(
                answers__answer=answer_id
            ),
            values=dict(
                expressions=dict(
                    audio_answer=F('answers__audio'),
                ),
                fields=[
                    'id', 'type', 'header', 'description',
                    'thematic_speech_content'
                ],
            ),
        ).order_by('answers__task_number',)


class QuestionRepository(BaseModelRepository):
    """Репозиторий для работы с вопросами в задании."""

    _model = Question

    def get_questions_by_task_answer(self, answer_id, task_id):
        """Получить информацию о вопросах в ответе на задание."""
        return self._read(
            filters=dict(
                answers__task__answer=answer_id,
                answers__task__task=task_id,
            ),
            values=dict(
                expressions=dict(
                    number=F('answers__question_number'),
                    audio_answer=F('answers__audio'),
                ),
                fields=[
                    'description', 'audio_answer',
                ],
            )
        ).order_by('answers__question_number',)


class ImageRepository(BaseModelRepository):
    """Репозиторий для работы с изображениями в задании."""

    _model = Image

    def get_images_by_task(self, task_id):
        """Получить информацию об изображениях в задании."""
        return self._read(
            filters=dict(
                parent_tasks__task=task_id,
            ),
            values=dict(
                fields=[
                    'header', 'image'
                ],
            )
        ).order_by('parent_tasks__number',)


class AnswerRepository(BaseModelRepository):
    """Репозиторий для работы с ответами."""

    _model = Answer

    def add_answer(self, user=None):
        """Добавить ответ."""
        return self._write(user=user)


class TaskAnswerRepository(BaseModelRepository):
    """Репозиторий для работы с заданиями в ответах."""

    _model = TaskAnswer

    def add_task_answer(self, answer_id, task_id, task_number, audio=None):
        """Добавить ответ."""
        return self._write(
            answer=Answer(answer_id),
            task=Task(task_id),
            task_number=task_number,
            audio=audio
        )


class QuestionAnswerRepository(BaseModelRepository):
    """Репозиторий для работы с вопросами в ответах."""

    _model = QuestionAnswer

    def add_question_answer(
            self, task_answer_id, question_id, question_number, audio
    ):
        """Добавить ответ."""
        return self._write(
            task=TaskAnswer(task_answer_id),
            question=Question(question_id),
            question_number=question_number,
            audio=audio
        )

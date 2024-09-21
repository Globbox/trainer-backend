import os

from django.conf import settings
from django.db.transaction import atomic

from trainer_backend.core.common.data_provider import (
    AbstractCreateDataProvider)
from trainer_backend.core.common.data_provider import AbstractReadDataProvider
from trainer_backend.trainer.mixins import AddTaskParametersMixin

from .repositories import AnswerRepository
from .repositories import ImageRepository
from .repositories import QuestionAnswerRepository
from .repositories import QuestionRepository
from .repositories import TaskAnswerRepository
from .repositories import TaskRepository


class AnswerTaskCreateDataProvider(AbstractCreateDataProvider):
    """Провайдер данных для добавления ответа."""

    answer_repository_class = AnswerRepository
    task_answer_repository_class = TaskAnswerRepository
    question_answer_repository_class = QuestionAnswerRepository

    def __init__(self):
        super().__init__()
        self._answer_repository = self.answer_repository_class()
        self._task_answer_repository = self.task_answer_repository_class()
        self._question_answer_repository = (
            self.question_answer_repository_class()
        )

    @atomic
    def set(self, tasks, user=None):
        """Добавить ответ."""
        answer = self._answer_repository.add_answer(user=user)

        for task_number, task in enumerate(tasks):
            task_answer = self._task_answer_repository.add_task_answer(
                answer.id,
                task.get('task_id'),
                task_number,
                audio=task.get('audio', None),
            )

            if task.get('questions'):
                for question_number, question in enumerate(
                        task.get('questions')
                ):
                    self._question_answer_repository.add_question_answer(
                        task_answer.id,
                        question.get('question_id'),
                        question_number,
                        question.get('audio')
                    )
        return answer


class AnswerTaskReadDataProvider(
    AddTaskParametersMixin, AbstractReadDataProvider
):
    """Провайдер данных для ответов на задания."""

    task_repository_class = TaskRepository
    question_repository_class = QuestionRepository
    image_repository_class = ImageRepository

    def __init__(self):
        super().__init__()
        self._task_repository = self.task_repository_class()
        self._question_repository = self.question_repository_class()
        self._image_repository = self.image_repository_class()

    @staticmethod
    def _add_full_file_path(
            instance, file_path_field, base_folder='media',
            new_field='full_file_path'
    ):
        """Получить полное имя файла."""
        if instance.get(file_path_field):
            instance[new_field] = os.path.join(
                base_folder, instance.get(file_path_field)
            )
        return instance

    def get(self, answer_id):
        """Получить данные по заданиям для ответа."""
        answer_data = []
        for task in self._task_repository.get_tasks_by_answer(answer_id):
            task['questions'] = [
                self._add_full_file_path(
                    question,
                    'audio_answer',
                    base_folder=settings.MEDIA_ROOT,
                    new_field='audio'
                )
                for question in (
                    self._question_repository.get_questions_by_task_answer(
                        answer_id, task['id']
                    )
                )
            ]

            task['images'] = [
                dict(header=image['header'], url=image['image'])
                for image in (
                    self._image_repository.get_images_by_task(task['id'])
                )
            ]
            task = self._add_full_file_path(
                task, 'audio_answer',
                base_folder=settings.MEDIA_ROOT,
                new_field='audio'
            )
            answer_data.append(
                self.add_task_number(task['type'], task)
            )

        return answer_data

from io import BytesIO
from os.path import join
import os
import re
import uuid
import zipfile

from django.conf import settings
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
from markdown import markdown
from weasyprint import HTML

from trainer_backend.core.common.usecase import AbstractUseCase

from .data_providers import AnswerTaskReadDataProvider
from .mappers import TaskTypeTemplateMapper
from .models import Answer


class GenerateAnswerArchive(AbstractUseCase):
    """Сгенерировать архив по заданиям."""

    _pdf_template = 'pdf_tasks_answer.html'
    _answer_data_provider_class = AnswerTaskReadDataProvider

    def __init__(self):
        self._answer_data_provider = self._answer_data_provider_class()

    @staticmethod
    def _add_markdown(instance, fields):
        """Добавить HTML теги для markdown полей."""
        clean = re.compile(r'</?p>')
        for field in fields:
            if isinstance(field, str):
                instance[field] = re.sub(
                    clean, '', markdown(instance[field], extensions=[])
                )
        return instance

    @staticmethod
    def _get_media_file_path(file_path):
        """Получить имя файла."""
        return f'file://{join(settings.MEDIA_ROOT, file_path)}'

    def _render_task_html(self, task):
        """Сформировать шаблон для задания."""
        task['images'] = [
            {**image, **{'url': self._get_media_file_path(image['url'])}}
            for image in task['images']
        ]
        template_path = TaskTypeTemplateMapper.get(task['type'])
        return render_to_string(template_path, task)

    def _create_pdf(self, tasks):
        """Сформировать PDF."""
        task_templates = [
            self._render_task_html(
                self._add_markdown(task, ('header', 'description',))
            )
            for task in tasks
        ]

        html_string = render_to_string(
            self._pdf_template,
            {'task_templates': task_templates},
        )
        pdf_buffer = BytesIO()
        HTML(string=html_string).write_pdf(pdf_buffer)
        return pdf_buffer

    @staticmethod
    def _get_answer_file_path(name, number, extra_number):
        """Сформировать имя файла."""
        return f'{name}_{number}_({extra_number}).mp3'

    def execute(self, answer_id, request=None):
        """Основной метод генерации данных."""
        tasks = self._answer_data_provider.get(answer_id)
        print(tasks)
        zip_buffer = BytesIO()
        with zipfile.ZipFile(
                zip_buffer, 'w', zipfile.ZIP_DEFLATED
        ) as zip_file:
            pdf_buffer = self._create_pdf(tasks)
            pdf_buffer.seek(0)

            zip_file.writestr('tasks.pdf', pdf_buffer.read())

            for i, task in enumerate(tasks):
                if task.get('audio') and os.path.isfile(task.get('audio')):
                    zip_file.write(
                        task.get('audio'),
                        self._get_answer_file_path(
                            'task', task['number'], i + 1
                        )
                    )

                if task.get('questions'):
                    for j, question in enumerate(task.get('questions')):
                        if question.get('audio') and os.path.isfile(
                                question.get('audio')
                        ):
                            zip_file.write(
                                question.get('audio'),
                                self._get_answer_file_path(
                                    f"task_{task['number']}_question",
                                    question['number'],
                                    i + 1
                                )
                            )
        zip_buffer.seek(0)

        Answer.objects.get(pk=answer_id).answer_archive.save(
            str(uuid.uuid4()) + '.zip', ContentFile(zip_buffer.read())
        )

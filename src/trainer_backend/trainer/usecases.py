from abc import ABC
from abc import abstractmethod
from io import BytesIO
import os
import uuid
import zipfile

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile

from django.template.loader import render_to_string
from pydub import AudioSegment
from weasyprint import HTML

from trainer_backend.core.common.usecase import AbstractUseCase
from trainer_backend.core.file.mixins import AudioFileConvertMixin
from trainer_backend.core.file.mixins import FileHashMixin

from .enums import AnswerStatus
from .mappers import TASK_TYPE_TEMPLATE_MAPPER
from .models import Answer
from .serializers import TaskAnswerSerializer


class BaseAnswerProcessUseCase(AbstractUseCase, ABC):
    """Базовый класс обработки ответа."""

    final_status: AnswerStatus

    def __init__(self):
        if self.final_status is None or (
            not isinstance(self.final_status, AnswerStatus)
        ):
            raise ValueError('не верно задан final_status')

    @abstractmethod
    def _process(self, answer: Answer):
        """Функция для обработки ответа."""

    def execute(self, answer_id, *args, **kwargs):
        """Основной метод обработки ответа."""
        answer = Answer.objects.get(pk=answer_id)
        self._process(answer)
        answer.status = self.final_status
        answer.save()


class ProcessAnswerUseCase(
    AudioFileConvertMixin, FileHashMixin, BaseAnswerProcessUseCase
):
    """Обработка аудио данных ответа."""

    final_status = AnswerStatus.AUDIO_PROCESSED

    def _convert_answer_audio(self, audio_field):
        """Конвертировать аудио данные."""
        old_file_path = audio_field.path
        converted_file = self.convert_audio(audio_field)
        new_file_path = self.get_file_hash_name(
            converted_file, with_dir=False
        )
        audio_field.save(new_file_path, converted_file)
        if os.path.exists(old_file_path):
            os.remove(old_file_path)

    @staticmethod
    def _concatenate_audio(audio_files):
        """Сформировать MP3 ответа."""
        concatenate_audio = AudioSegment.empty()

        for audio_file in audio_files:
            concatenate_audio += AudioSegment.from_file(
                BytesIO(audio_file.read())
            )

        output_buffer = BytesIO()
        concatenate_audio.export(output_buffer, format="mp3")
        output_buffer.seek(0)
        return SimpleUploadedFile(
            name=f'{uuid.uuid4()}.mp3',
            content=output_buffer.read(),
            content_type='audio/mp3'
        )

    def _process(self, answer: Answer):
        """Функция для обработки ответа."""
        audio_files = []
        for task in answer.tasks.order_by('task_number'):
            if bool(task.audio):
                self._convert_answer_audio(task.audio)
                audio_files.append(task.audio)

            for question in task.questions.order_by('question_number'):
                if bool(question.audio):
                    self._convert_answer_audio(question.audio)
                    audio_files.append(question.audio)
        full_audio = self._concatenate_audio(audio_files)
        answer.full_audio.save(
            self.get_file_hash_name(full_audio),
            full_audio
        )


class AnswerPdfGeneratorUseCase(AbstractUseCase):
    """UseCase для генерации PDF файла."""

    _pdf_template = 'pdf_tasks_answer.html'

    @staticmethod
    def _render_task_html(task):
        """Сформировать шаблон для задания."""
        template_path = TASK_TYPE_TEMPLATE_MAPPER.get(task.task.task_type)
        return render_to_string(
            template_path,
            TaskAnswerSerializer(
                task, context={'with_tasks': True}
            ).data
        )

    def execute(self, answer: Answer, *args, **kwargs):
        """Сгенерировать PDF файл."""
        task_templates = []
        for task in answer.tasks.order_by('task_number'):
            task_templates.append(
                self._render_task_html(task)
            )

        html_string = render_to_string(
            self._pdf_template,
            {'task_templates': task_templates},
        )
        pdf_buffer = BytesIO()
        HTML(string=html_string).write_pdf(pdf_buffer)
        pdf_buffer.seek(0)
        return pdf_buffer


class GenerateAnswerArchiveUseCase(BaseAnswerProcessUseCase):
    """Сгенерировать архив по заданиям."""

    final_status = AnswerStatus.PROCESSED

    def _process(self, answer: Answer, *args, **kwargs):
        """Основной метод генерации данных."""
        zip_buffer = BytesIO()
        with zipfile.ZipFile(
                zip_buffer, 'w', zipfile.ZIP_DEFLATED
        ) as zip_file:
            # Генерируем PDF файл ответа
            pdf_buffer = AnswerPdfGeneratorUseCase().execute(answer)
            pdf_buffer.seek(0)

            zip_file.writestr('tasks.pdf', pdf_buffer.read())
            zip_file.writestr(
                'tasks_audio.mp3', answer.full_audio.read()
            )
        zip_buffer.seek(0)
        answer.answer_archive.save(
            str(uuid.uuid4()) + '.zip', ContentFile(zip_buffer.read())
        )

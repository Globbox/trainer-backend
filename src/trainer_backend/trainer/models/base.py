from django.conf import settings
from django.db import models

from trainer_backend.core.db.mixins import ShortDescriptionMixin
from trainer_backend.core.file.mixins import AudioFileConvertMixin
from trainer_backend.core.file.utils import upload_hash_file
from trainer_backend.trainer.enums import ExamType
from trainer_backend.trainer.enums import TaskType


class Image(models.Model):
    """Модель для хранения изображений."""

    header = models.CharField(
        max_length=100,
        verbose_name='Заголовок',
    )

    image = models.FileField(
        upload_to=upload_hash_file(
            'image',
            settings.IMAGE_TASK_DIR,
        ),
        verbose_name='Изображение',
    )

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


class Exam(models.Model):
    """Модель Экзаменов."""

    number = models.PositiveIntegerField(
        verbose_name="Номер экзамена"
    )
    fipi = models.BooleanField(
        default=False,
        verbose_name="Экзамен из банка ФИПИ"
    )
    type = models.SmallIntegerField(
        choices=ExamType.choices(),
        verbose_name="Тип экзамена"
    )

    def __str__(self):
        return f'Экзамен {self.number}'

    class Meta:
        unique_together = (('number', 'type'),)
        verbose_name = "Экзамен"
        verbose_name_plural = "Экзамены"


class ThematicSpeechContent(models.Model, ShortDescriptionMixin):
    """Модель тематического содержания речи."""

    description_field = 'description'

    @staticmethod
    def get_russian_alphabet_tuples():
        """Получить буквы русского алфавита в виде tuples."""
        first_symbol = ord('А')
        alphabet = [chr(i) for i in range(first_symbol, first_symbol + 32)]

        return [a for a in zip(alphabet, alphabet)]

    short_designation = models.CharField(
        max_length=1,
        verbose_name="Краткое обозначение",
        choices=get_russian_alphabet_tuples(),
        unique=True,
    )

    description = models.TextField(
        verbose_name='Описание',
    )

    def __str__(self):
        return f'{self.short_designation}. {self.get_short_description()}'

    class Meta:
        verbose_name = "Тематическое содержание речи"
        verbose_name_plural = "Тематические содержания речи"


class Task(AudioFileConvertMixin, ShortDescriptionMixin, models.Model):
    """Модель Задание."""

    description_field = 'header'

    type = models.SmallIntegerField(
        choices=TaskType.choices(),
        verbose_name='Тип задания',
    )
    header = models.TextField(
        verbose_name='Заголовок',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
    )
    thematic_speech_content = models.ForeignKey(
        ThematicSpeechContent,
        on_delete=models.PROTECT,
        related_name='tasks',
        verbose_name='Тематическое содержания речи',
    )
    audio = models.FileField(
        null=True,
        blank=True,
        upload_to=upload_hash_file(
            'audio',
            settings.AUDIO_TASK_DIR,
        ),
        verbose_name='Аудио задание',
    )

    def __str__(self):
        return f'Задание. {self.get_short_description()}'

    def clean(self):
        """Обработка перед изменением/добавлением."""
        super().clean()
        if bool(self.audio):
            self.audio = self.convert_audio(self.audio)

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"


class Question(AudioFileConvertMixin, ShortDescriptionMixin, models.Model):
    """Модель вопросов."""

    description_field = 'description'

    description = models.TextField(
        blank=True,
        verbose_name='Описание',
    )
    audio = models.FileField(
        null=True,
        blank=True,
        upload_to=upload_hash_file(
            'audio',
            settings.AUDIO_TASK_DIR,
        ),
        verbose_name='Аудио задание',
    )

    def clean(self):
        """Обработка перед изменением/добавлением."""
        super().clean()
        if bool(self.audio):
            self.audio = self.convert_audio(self.audio)

    def __str__(self):
        if self.description:
            return (
                f'Текстовый вопрос {self.pk}. {self.get_short_description()}'
            )
        return f'Аудио вопрос {self.pk}'

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

import os

from django.db import models
from django.dispatch import receiver

from trainer_backend.core.db.mixins import ShortDescriptionMixin
from trainer_backend.core.file.mixins import AudioFileConvertMixin
from trainer_backend.core.file.mixins import FileHashMixin
from trainer_backend.trainer.enums import ExamType
from trainer_backend.trainer.enums import TaskType


class ModelWithFileMixin(FileHashMixin):
    """Миксин для моделей с файлами."""

    file_field: str = None

    def save(self, *args, **kwargs):
        """Сохранение/изменение записи."""
        file = getattr(self, self.file_field)
        if not file:
            return super().save(*args, **kwargs)

        old_file = None
        if self.pk:
            old_instance = self.__class__.objects.get(pk=self.pk)
            old_file = getattr(old_instance, self.file_field)

        if old_file and old_file.name != file.name:
            old_file_path = old_file.path
            if os.path.exists(old_file_path):
                os.remove(old_file_path)

        new_file_path = self.get_file_hash_name(file)
        setattr(file, 'name', new_file_path)
        return super().save(*args, **kwargs)


class ModelWithAudioFileMixin(ModelWithFileMixin, AudioFileConvertMixin):
    """Миксин для моделей с аудио файлами."""

    file_field: str = 'audio'

    def save(self, *args, **kwargs):
        """Сохранение/изменение записи."""
        file = getattr(self, self.file_field)
        if file:
            setattr(self, self.file_field, self.convert_audio(file))
        super().save(*args, **kwargs)


class Image(ModelWithFileMixin, models.Model):
    """Модель для хранения изображений."""

    file_field = 'image'

    header = models.CharField(
        max_length=100,
        verbose_name='Заголовок',
    )

    image = models.FileField(
        upload_to='guidance/',
        verbose_name='Изображение',
    )

    def save(self, *args, **kwargs):
        """Сохранение/изменения записи."""
        if not self.pk or (
            self.image != self.__class__.objects.get(pk=self.pk).image
        ):
            self.image.name = self.get_file_hash_name(self.image)
        super().save(*args, **kwargs)

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
    exam_type = models.SmallIntegerField(
        choices=ExamType.choices(),
        verbose_name="Тип экзамена"
    )

    def __str__(self):
        return f'Экзамен {self.number}'

    class Meta:
        unique_together = (('number', 'exam_type'),)
        verbose_name = "Экзамен"
        verbose_name_plural = "Экзамены"


class ThematicSpeechContent(ShortDescriptionMixin, models.Model):
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


class Task(ModelWithAudioFileMixin, ShortDescriptionMixin, models.Model):
    """Модель Задание."""

    description_field = 'header'

    task_type = models.SmallIntegerField(
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
        upload_to='guidance/',
        verbose_name='Аудио задание',
    )

    def __str__(self):
        return f'Задание. {self.get_short_description()}'

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"


class Question(ModelWithAudioFileMixin, ShortDescriptionMixin, models.Model):
    """Модель вопросов."""

    description_field = 'description'

    description = models.TextField(
        verbose_name='Описание',
    )
    audio = models.FileField(
        null=True,
        blank=True,
        upload_to='guidance/',
        verbose_name='Аудио задание',
    )

    def __str__(self):
        return f'Вопрос задания. {self.get_short_description()}'

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


@receiver(models.signals.post_delete, sender=Question)
@receiver(models.signals.post_delete, sender=Task)
def auto_delete_audio_file(sender, instance, **kwargs):
    """Удаление файла при удалении записи."""
    if instance.audio:
        instance.audio.delete(save=False)


@receiver(models.signals.post_delete, sender=Image)
def auto_delete_image_file(sender, instance, **kwargs):
    """Удаление файла при удалении записи."""
    if instance.image:
        instance.image.delete(save=False)

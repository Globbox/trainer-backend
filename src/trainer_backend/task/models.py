from django.db import models
from trainer_backend.task.enums import MediaTypeEnum


class Task(models.Model):
    """Модель для работы с заданиями."""

    header = models.CharField(
        max_length=1024,
        verbose_name='Заголовок задания',
    )
    assignment = models.TextField(
        verbose_name='Текст задания',
    )
    media_type = models.SmallIntegerField(
        choices=MediaTypeEnum.choices(),
        default=MediaTypeEnum.NO_MEDIA,
        verbose_name='Тип медиа данных'
    )
    media_path = models.CharField(
        verbose_name='Путь до медиа данных',
        max_length=1024,
        null=True,
    )
    seconds_to_prepare = models.IntegerField(
        verbose_name='Кол-во секунд на подготовку',
    )
    seconds_to_answer = models.IntegerField(
        verbose_name='Кол-во секунд на ответ',
    )

    class Meta:
        verbose_name = 'Задача'


class TaskGroup(models.Model):
    """Модель для работы с вариантами."""

    number = models.CharField(
        verbose_name='Номер варианта',
        max_length=64,
    )

    class Meta:
        verbose_name = 'Группа задач'
        indexes = [
            models.Index(
                name='%(app_label)s_%(class)s_number',
                fields=['number'],
            )
        ]


class TaskGroupBinding(models.Model):
    """"""

    group = models.ForeignKey(
        TaskGroup,
        on_delete=models.CASCADE
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE
    )



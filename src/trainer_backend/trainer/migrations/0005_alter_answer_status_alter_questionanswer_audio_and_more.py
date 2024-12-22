# Generated by Django 5.0.2 on 2024-12-01 16:54

from django.db import migrations
from django.db import models

import trainer_backend.trainer.enums


class Migration(migrations.Migration):
    dependencies = [
        ('trainer', '0004_remove_answer_processed_answer_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='status',
            field=models.SmallIntegerField(choices=[
                (trainer_backend.trainer.enums.AnswerStatus['UNPROCESSED'],
                 'Необработан'),
                (trainer_backend.trainer.enums.AnswerStatus['AUDIO_PROCESSED'],
                 'Аудио данные обработаны'),
                (trainer_backend.trainer.enums.AnswerStatus['PROCESSED'],
                 'Обработан')
            ], default=1),
        ),
        migrations.AlterField(
            model_name='questionanswer',
            name='audio',
            field=models.FileField(upload_to='answer/',
                                   verbose_name='Ответ на вопрос'),
        ),
        migrations.AlterField(
            model_name='taskanswer',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to='answer/',
                                   verbose_name='Ответ на задание'),
        ),
    ]

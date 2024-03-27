# Generated by Django 5.0.3 on 2024-03-15 20:35

import django.db.models.deletion
import trainer_backend.task.enums
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=1024, verbose_name='Заголовок задания')),
                ('assignment', models.TextField(verbose_name='Текст задания')),
                ('media_type', models.SmallIntegerField(choices=[(trainer_backend.task.enums.MediaTypeEnum['NO_MEDIA'], 'Без медиа данных'), (trainer_backend.task.enums.MediaTypeEnum['IMAGE'], 'Картинка'), (trainer_backend.task.enums.MediaTypeEnum['SOUND'], 'Звук')], default=trainer_backend.task.enums.MediaTypeEnum['NO_MEDIA'], verbose_name='Тип медиа данных')),
                ('media_path', models.CharField(max_length=1024, null=True, verbose_name='Путь до медиа данных')),
                ('seconds_to_prepare', models.IntegerField(verbose_name='Кол-во секунд на подготовку')),
                ('seconds_to_answer', models.IntegerField(verbose_name='Кол-во секунд на ответ')),
            ],
            options={
                'verbose_name': 'Задача',
                'indexes': [models.Index(fields=['media_type'], name='task_task_media_type')],
            },
        ),
        migrations.CreateModel(
            name='TaskGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=64, verbose_name='Номер варианта')),
            ],
            options={
                'verbose_name': 'Группа задач',
                'indexes': [models.Index(fields=['number'], name='task_taskgroup_number')],
            },
        ),
        migrations.CreateModel(
            name='TaskGroupBinding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.taskgroup')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.task')),
            ],
        ),
    ]
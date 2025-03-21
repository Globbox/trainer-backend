# Generated by Django 5.0.2 on 2024-11-14 21:30

from django.db import migrations
from django.db import models

import trainer_backend.core.db.mixins
import trainer_backend.trainer.enums
import trainer_backend.trainer.models.base


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('processed', models.BooleanField(default=False)),
                ('full_audio', models.FileField(blank=True, null=True, upload_to='answer/', verbose_name='Полный ответ пользователя')),
                ('answer_archive', models.FileField(blank=True, null=True, upload_to='answer/', verbose_name='Архив ответа')),
            ],
            options={
                'verbose_name': 'Ответ пользователя',
                'verbose_name_plural': 'Ответы пользователя',
            },
        ),
        migrations.CreateModel(
            name='AudioGuidance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guidance_type', models.PositiveSmallIntegerField(choices=[(trainer_backend.trainer.enums.AudioGuidanceType['START_EXAM'], 'Перед началом экзамена'), (trainer_backend.trainer.enums.AudioGuidanceType['END_EXAM'], 'После окончания экзамена'), (trainer_backend.trainer.enums.AudioGuidanceType['BEFORE_TASK_EXECUTION'], 'Перед началом выполнения задания'), (trainer_backend.trainer.enums.AudioGuidanceType['AFTER_TASK_EXECUTION'], 'После окончания выполнения задания'), (trainer_backend.trainer.enums.AudioGuidanceType['BEFORE_QUESTION_EXECUTION'], 'Перед началом ответа на вопрос'), (trainer_backend.trainer.enums.AudioGuidanceType['AFTER_QUESTION_EXECUTION'], 'После окончания ответа на вопрос')], unique=True, verbose_name='Тип аудио сопровождения')),
                ('audio', models.FileField(upload_to='guidance/', verbose_name='Аудио файл')),
            ],
            options={
                'verbose_name': 'Аудио сопровождение',
                'verbose_name_plural': 'Аудио сопровождения',
            },
            bases=(trainer_backend.trainer.models.base.ModelWithAudioFileMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(verbose_name='Номер экзамена')),
                ('fipi', models.BooleanField(default=False, verbose_name='Экзамен из банка ФИПИ')),
                ('exam_type', models.SmallIntegerField(choices=[(trainer_backend.trainer.enums.ExamType['EGE'], 'ЕГЭ'), (trainer_backend.trainer.enums.ExamType['OGE'], 'ОГЭ')], verbose_name='Тип экзамена')),
            ],
            options={
                'verbose_name': 'Экзамен',
                'verbose_name_plural': 'Экзамены',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('image', models.FileField(upload_to='guidance/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
            bases=(trainer_backend.trainer.models.base.ModelWithFileMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ImagesInTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(verbose_name='Порядок изображений в задании')),
            ],
            options={
                'verbose_name': 'Изображения в задании',
                'verbose_name_plural': 'Изображений в задании',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Описание')),
                ('audio', models.FileField(blank=True, null=True, upload_to='guidance/', verbose_name='Аудио задание')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
            bases=(trainer_backend.trainer.models.base.ModelWithAudioFileMixin, trainer_backend.core.db.mixins.ShortDescriptionMixin, models.Model),
        ),
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_number', models.PositiveIntegerField(null=True, verbose_name='Номер вопроса')),
                ('audio', models.FileField(upload_to='answer/', verbose_name='Аудио задание')),
            ],
            options={
                'verbose_name': 'Ответ пользователя к вопросу',
                'verbose_name_plural': 'Ответы пользователя к вопросам',
            },
        ),
        migrations.CreateModel(
            name='QuestionAudioGuidance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_number', models.PositiveIntegerField(unique=True, verbose_name='Номер вопроса')),
                ('audio', models.FileField(upload_to='guidance/', verbose_name='Аудио файл')),
            ],
            options={
                'verbose_name': 'Аудио сопровождение вопросов',
                'verbose_name_plural': 'Аудио сопровождения вопросов',
            },
            bases=(trainer_backend.trainer.models.base.ModelWithAudioFileMixin, models.Model),
        ),
        migrations.CreateModel(
            name='QuestionsInTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(verbose_name='Порядок вопросов в задании')),
            ],
            options={
                'verbose_name': 'Вопрос в задании',
                'verbose_name_plural': 'Вопросы в задании',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_type', models.SmallIntegerField(choices=[(trainer_backend.trainer.enums.TaskType['SPEAKING'], 'Разговорный'), (trainer_backend.trainer.enums.TaskType['STUDY_THE_ADVERTISEMENT'], 'Изучение рекламы'), (trainer_backend.trainer.enums.TaskType['INTERVIEW'], 'Интервью'), (trainer_backend.trainer.enums.TaskType['IMAGE_SPEAKING'], 'Разговорный с изображениями')], verbose_name='Тип задания')),
                ('header', models.TextField(verbose_name='Заголовок')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('audio', models.FileField(blank=True, null=True, upload_to='guidance/', verbose_name='Аудио задание')),
            ],
            options={
                'verbose_name': 'Задание',
                'verbose_name_plural': 'Задания',
            },
            bases=(trainer_backend.trainer.models.base.ModelWithAudioFileMixin, trainer_backend.core.db.mixins.ShortDescriptionMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TaskAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_number', models.PositiveIntegerField(null=True, verbose_name='Номер задания')),
                ('audio', models.FileField(blank=True, null=True, upload_to='answer/', verbose_name='Ответ на задание')),
            ],
            options={
                'verbose_name': 'Ответ пользователя к заданию',
                'verbose_name_plural': 'Ответы пользователя к заданиям',
            },
        ),
        migrations.CreateModel(
            name='TasksInExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Задание в экзамене',
                'verbose_name_plural': 'Задания в экзамене',
            },
        ),
        migrations.CreateModel(
            name='TaskTypeParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_type', models.SmallIntegerField(choices=[(trainer_backend.trainer.enums.TaskType['SPEAKING'], 'Разговорный'), (trainer_backend.trainer.enums.TaskType['STUDY_THE_ADVERTISEMENT'], 'Изучение рекламы'), (trainer_backend.trainer.enums.TaskType['INTERVIEW'], 'Интервью'), (trainer_backend.trainer.enums.TaskType['IMAGE_SPEAKING'], 'Разговорный с изображениями')], unique=True, verbose_name='Тип задания')),
                ('number', models.PositiveIntegerField(verbose_name='Порядок задания в экзамене')),
                ('audio', models.FileField(upload_to='guidance/', verbose_name='Аудио сопровождение')),
                ('preparation_seconds', models.PositiveIntegerField(verbose_name='Кол-во секунд на подготовку задания')),
                ('execution_seconds', models.PositiveIntegerField(blank=True, null=True, verbose_name='Кол-во секунд на выполнение задания')),
                ('question_execution_seconds', models.PositiveIntegerField(blank=True, null=True, verbose_name='Кол-во секунд на ответ')),
            ],
            options={
                'verbose_name': 'Параметр для типов заданий',
                'verbose_name_plural': 'Параметры для типов заданий',
            },
            bases=(trainer_backend.trainer.models.base.ModelWithAudioFileMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ThematicSpeechContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_designation', models.CharField(choices=[('А', 'А'), ('Б', 'Б'), ('В', 'В'), ('Г', 'Г'), ('Д', 'Д'), ('Е', 'Е'), ('Ж', 'Ж'), ('З', 'З'), ('И', 'И'), ('Й', 'Й'), ('К', 'К'), ('Л', 'Л'), ('М', 'М'), ('Н', 'Н'), ('О', 'О'), ('П', 'П'), ('Р', 'Р'), ('С', 'С'), ('Т', 'Т'), ('У', 'У'), ('Ф', 'Ф'), ('Х', 'Х'), ('Ц', 'Ц'), ('Ч', 'Ч'), ('Ш', 'Ш'), ('Щ', 'Щ'), ('Ъ', 'Ъ'), ('Ы', 'Ы'), ('Ь', 'Ь'), ('Э', 'Э'), ('Ю', 'Ю'), ('Я', 'Я')], max_length=1, unique=True, verbose_name='Краткое обозначение')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Тематическое содержание речи',
                'verbose_name_plural': 'Тематические содержания речи',
            },
            bases=(trainer_backend.core.db.mixins.ShortDescriptionMixin, models.Model),
        ),
    ]

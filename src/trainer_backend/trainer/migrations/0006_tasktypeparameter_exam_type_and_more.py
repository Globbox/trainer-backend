import trainer_backend.trainer.enums
from django.db import migrations
from django.db import models
from trainer_backend.trainer.enums import ExamType


def update_current_task_type_parameters(apps, _):
    """Обновление данных."""
    apps.get_model(
        'trainer', 'TaskTypeParameter'
    ).objects.update(
        exam_type=ExamType.EGE
    )


class Migration(migrations.Migration):
    dependencies = [
        ('trainer',
         '0005_alter_answer_status_alter_questionanswer_audio_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasktypeparameter',
            name='exam_type',
            field=models.SmallIntegerField(choices=[
                (trainer_backend.trainer.enums.ExamType['EGE'], 'ЕГЭ'),
                (trainer_backend.trainer.enums.ExamType['OGE'], 'ОГЭ')],
                default=None,
                verbose_name='Тип экзамена'),
        ),
        migrations.AlterField(
            model_name='audioguidance',
            name='guidance_type',
            field=models.PositiveSmallIntegerField(choices=[(
                trainer_backend.trainer.enums.AudioGuidanceType[
                    'START_EXAM'],
                'Перед началом экзамена'),
                (
                    trainer_backend.trainer.enums.AudioGuidanceType[
                        'END_EXAM'],
                    'После окончания экзамена'),
                (
                    trainer_backend.trainer.enums.AudioGuidanceType[
                        'BEFORE_TASK_EXECUTION'],
                    'Перед началом выполнения задания'),
                (
                    trainer_backend.trainer.enums.AudioGuidanceType[
                        'AFTER_TASK_EXECUTION'],
                    'После окончания выполнения задания'),
                (
                    trainer_backend.trainer.enums.AudioGuidanceType[
                        'BEFORE_QUESTION_EXECUTION'],
                    'Перед началом ответа на вопрос'),
                (
                    trainer_backend.trainer.enums.AudioGuidanceType[
                        'AFTER_QUESTION_EXECUTION'],
                    'После окончания ответа на вопрос'),
                (
                    trainer_backend.trainer.enums.AudioGuidanceType[
                        'START_INTERVIEW'],
                    'Перед началом интервью'),
                (
                    trainer_backend.trainer.enums.AudioGuidanceType[
                        'END_INTERVIEW'],
                    'После окончания интервью'),
                (
                    trainer_backend.trainer.enums.AudioGuidanceType[
                        'BETWEEN_QUESTION'],
                    'Между вопросами')],
                unique=True,
                verbose_name='Тип аудио сопровождения'),
        ),
        migrations.RunPython(update_current_task_type_parameters),
        migrations.AlterField(
            model_name='tasktypeparameter',
            name='exam_type',
            field=models.SmallIntegerField(
                choices=[
                    (trainer_backend.trainer.enums.ExamType['EGE'], 'ЕГЭ'),
                    (trainer_backend.trainer.enums.ExamType['OGE'], 'ОГЭ')
                ], verbose_name='Тип экзамена'
            ),
        ),
        migrations.AlterUniqueTogether(
            name='tasktypeparameter',
            unique_together={('exam_type', 'task_type', 'number')},
        ),
        migrations.AlterField(
            model_name='tasktypeparameter',
            name='task_type',
            field=models.SmallIntegerField(
                choices=[(
                    trainer_backend.trainer.enums.TaskType['SPEAKING'],
                    'Разговорный'), (
                    trainer_backend.trainer.enums.TaskType[
                        'STUDY_THE_ADVERTISEMENT'],
                    'Изучение рекламы'), (
                    trainer_backend.trainer.enums.TaskType[
                        'INTERVIEW'],
                    'Интервью'), (
                    trainer_backend.trainer.enums.TaskType[
                        'IMAGE_SPEAKING'],
                    'Разговорный с изображениями')],
                verbose_name='Тип задания'),
        ),
    ]

from rest_framework import serializers
from trainer_backend.task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор модели Задания."""

    media_type = serializers.IntegerField()

    class Meta:
        model = Task
        fields = '__all__'


class MediaTaskSerializer(TaskSerializer):
    """Сериализатор модели Задания с медиа данными."""

    data = serializers.FileField(
        allow_null=False
    )

    class Meta:
        model = Task
        fields = [
            'data'
        ]

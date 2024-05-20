from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from trainer_backend.task.models import Task
from trainer_backend.task.serializers import MediaTaskSerializer
from trainer_backend.task.serializers import TaskSerializer
from trainer_backend.task.enums import MediaTypeEnum
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
import os


class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с заданиями."""

    api_version = 1
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    lookup_value_regex = r'\d+'

    #
    # # def get_serializer(self, *args, **kwargs):
    # #     """Получить сериализатор данных."""
    # #     # media_type = media_type or MediaTypeEnum.NO_MEDIA
    # #     #
    # #     # serializer_class = self.get_serializer_class()
    # #     # kwargs.setdefault('context', self.get_serializer_context())
    # #     return MediaTaskSerializer(*args, **kwargs, many=False)
    def list(self, request, *args, **kwargs):
        return self.get_queryset()

    def create(self, request, *args, **kwargs):
        #     self.queryset.create(
        #         **request.data
        #     )
        #     return Response(data={})
        # #     # print(data)
        file_data = request.data.get('data')

        directory = os.path.dirname(
            os.path.join(settings.MEDIA_ROOT, 'tasks')
        )

        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        file_path = os.path.join(directory, 'test_file.mp3')
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)

        with open(file_path, 'wb') as file:
            file.write(file_data.read())
        # serializer.save()
        # print(serializer.data)

        self.queryset.create(
            media_path=file_path,
            header='Header 1',
            assignment='Assignment text',
            seconds_to_prepare=10,
            seconds_to_answer=10
        )
        return Response(
            [],
            status=status.HTTP_201_CREATED,
            # headers=self.get_success_headers(serializer.data)
        )

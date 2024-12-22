from datetime import datetime
from functools import partial
from os import path
import hashlib
import io
import mimetypes
import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.html import format_html
from pydub import AudioSegment

from .enums import AudioFileTypeEnum


class AudioFileFieldAdminMixin:
    """Миксин добавляющий функционал для работы с аудио из админ панели."""

    audio_field = 'audio'
    audio_file_type = AudioFileTypeEnum.MP3

    def audio_preview(self, obj):
        """Прослушать аудио."""
        audio_file = getattr(obj, self.audio_field)

        if not audio_file:
            return "Аудио отсутствует"
        audio_file_type = self.audio_file_type.value
        return format_html(f"""
            <audio controls>
            <source
                src="{audio_file.url}"
                type="{audio_file_type['mime_type']}"
            >
            Браузер не поддерживает прослушивание аудио
            </audio>
        """)

    audio_preview.short_description = "Прослушать"


class AudioFileConvertMixin:
    """Миксин для конвертации аудио файлов перед сохранением в модель."""

    audio_file_type = AudioFileTypeEnum.MP3
    bitrate = 256

    def convert_audio(self, audio_file):
        """Конвертирует входной аудио файл в указанный формат."""
        file_name, file_ext = path.splitext(audio_file.name)
        mime_type, _ = mimetypes.guess_type(audio_file.url)
        audio_file_type = self.audio_file_type.value

        if mime_type == audio_file_type['mime_type']:
            return audio_file

        file_data = io.BytesIO(audio_file.read())
        audio_file.seek(0)

        try:
            audio = AudioSegment.from_file(file_data)
        except Exception as e:
            raise ValueError(f"Не удалось конвертировать файл: {e}")

        new_file_data = io.BytesIO()
        audio.export(
            new_file_data,
            format=audio_file_type['extension'].split('.')[1],
            bitrate=str(self.bitrate)
        )

        new_file_data.seek(0)
        return ContentFile(
            new_file_data.read(),
            name=f"{file_name}{audio_file_type['extension']}"
        )


class FileHashMixin:
    """Миксин для получения наименования по хеш-сумме файла."""

    block_size = 65536
    hash_func = hashlib.md5

    def get_file_hash_name(self, file, with_timestamp=True, with_dir=True):
        """Получить имя файла на основе хеш-суммы."""
        old_file_name, file_ext = path.splitext(file.name)
        file_dir = path.dirname(old_file_name)
        hasher = self.hash_func()

        if with_timestamp:
            hasher.update(str(datetime.now()).encode('utf-8'))

        file.seek(0)
        for buf in iter(partial(file.read, self.block_size), b''):
            hasher.update(buf)

        if with_dir:
            return path.join(
                file_dir, f'{hasher.hexdigest()}{file_ext}'
            )

        return f'{hasher.hexdigest()}{file_ext}'


class FilePathMixin:
    """Миксин для получения путей файла."""

    use_real_path: bool = False
    file_dir: str = settings.MEDIA_URL
    real_file_dir: str = settings.MEDIA_ROOT

    def _get_file_path(self, file_path):
        """Получить путь к объекту."""
        base_dir = self.file_dir
        if self.use_real_path:
            base_dir = self.real_file_dir

        return os.path.join(
            base_dir, file_path
        )

    def _add_file_path(self, instance, file_path_name):
        """Добавить объекту путь к файлу."""
        file_path = instance.get(file_path_name)
        if not file_path:
            return instance

        instance[file_path_name] = self._get_file_path(file_path)
        return instance

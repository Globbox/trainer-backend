from os import path
import io
import mimetypes

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

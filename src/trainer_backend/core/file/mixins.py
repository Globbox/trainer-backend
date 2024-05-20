from os import path
import io

from django.core.files.base import ContentFile
from django.utils.html import format_html
from pydub import AudioSegment


class AudioFileFieldAdminMixin:
    """Миксин добавляющий функционал для работы с аудио из админ панели."""

    audio_field = 'audio'

    def audio_preview(self, obj):
        """Прослушать аудио."""
        audio_file = getattr(obj, self.audio_field)

        if not audio_file:
            return "Аудио отсутствует"

        return format_html(f"""
            <audio controls>
            <source src="{audio_file.url}" type="audio/mpeg">
            Браузер не поддерживает прослушивание аудио
            </audio>
        """)

    audio_preview.short_description = "Прослушать"


class AudioFileConvertMixin:
    """Миксин для конвертации аудио файлов перед сохранением в модель."""

    format = 'mp3'
    bitrate = 256

    def convert_audio(self, audio_file):
        """Конвертирует входной аудио файл в указанный формат."""
        file_name, file_ext = path.splitext(audio_file.name)
        if file_ext.endswith(self.format):
            return audio_file

        file_data = io.BytesIO(audio_file.read())
        audio_file.seek(0)

        try:
            audio = AudioSegment.from_file(
                file_data,
                format=self.format
            )
        except Exception as e:
            raise ValueError(f"Не удалось конвертировать файл: {e}")

        new_file_data = io.BytesIO()
        audio.export(
            new_file_data, format=self.format, bitrate=str(self.bitrate)
        )

        new_file_data.seek(0)
        return ContentFile(
            new_file_data.read(),
            name=f"{file_name}.mp3"
        )

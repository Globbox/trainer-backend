from choicesenum import ChoicesEnum


class AudioFileTypeEnum(ChoicesEnum):
    """Enum для типов аудио файлов."""

    MP3 = {"extension": ".mp3", "mime_type": "audio/mpeg"}
    WAV = {"extension": ".wav", "mime_type": "audio/wav"}
    OGG = {"extension": ".ogg", "mime_type": "audio/ogg"}
    FLAC = {"extension": ".flac", "mime_type": "audio/flac"}
    AAC = {"extension": ".aac", "mime_type": "audio/aac"}
    M4A = {"extension": ".m4a", "mime_type": "audio/mp4"}
    WMA = {"extension": ".wma", "mime_type": "audio/x-ms-wma"}
    OPUS = {"extension": ".opus", "mime_type": "audio/opus"}
    AIFF = {"extension": ".aiff", "mime_type": "audio/aiff"}
    AMR = {"extension": ".amr", "mime_type": "audio/amr"}

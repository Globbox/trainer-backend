from choicesenum import ChoicesEnum


class MediaTypeEnum(ChoicesEnum):
    """Типы медиа данных."""

    NO_MEDIA = 0, 'Без медиа данных'
    IMAGE = 1, 'Картинка'
    SOUND = 2, 'Звук'

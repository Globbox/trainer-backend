from choicesenum import ChoicesEnum


class AudioGuidanceType(ChoicesEnum):
    """Типы аудио сопровождения."""

    START_EXAM = 1, 'Перед началом экзамена'
    END_EXAM = 2, 'После окончания экзамена'
    BEFORE_TASK_EXECUTION = 3, 'Перед началом выполнения задания'
    AFTER_TASK_EXECUTION = 4, 'После окончания выполнения задания'
    BEFORE_QUESTION_EXECUTION = 5, 'Перед началом ответа на вопрос'
    AFTER_QUESTION_EXECUTION = 6, 'После окончания ответа на вопрос'
    START_INTERVIEW = 7, 'Перед началом интервью'
    END_INTERVIEW = 8, 'После окончания интервью'


class TaskType(ChoicesEnum):
    """Типы заданий."""

    SPEAKING = 1, 'Разговорный'
    STUDY_THE_ADVERTISEMENT = 2, 'Изучение рекламы'
    INTERVIEW = 3, 'Интервью'
    IMAGE_SPEAKING = 4, 'Разговорный с изображениями'


class ExamType(ChoicesEnum):
    """Типы экзаменов."""

    EGE = 1, 'ЕГЭ'
    OGE = 2, 'ОГЭ'


class AnswerStatus(ChoicesEnum):
    """Статус ответа."""

    UNPROCESSED = 1, 'Необработан'
    AUDIO_PROCESSED = 2, 'Аудио данные обработаны'
    PROCESSED = 3, 'Обработан'

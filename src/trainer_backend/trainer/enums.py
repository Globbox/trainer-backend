from choicesenum import ChoicesEnum


class AudioGuidanceType(ChoicesEnum):
    """Типы аудио сопровождения."""

    START_EXAM = 1, 'Начало экзамена'
    END_EXAM = 2, 'Окончание экзамена'
    BEFORE_TASK_EXECUTION = 3, 'Начало выполнения задания'
    INTERVIEW_END = 4, 'Завершение интервью'


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

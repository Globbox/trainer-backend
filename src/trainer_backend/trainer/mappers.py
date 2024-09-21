from .enums import AudioGuidanceType
from .enums import TaskType


AUDIO_GUIDANCE_FIELD_MAPPER = {
    AudioGuidanceType.START_EXAM: 'start_exam_audio',
    AudioGuidanceType.END_EXAM: 'end_exam_audio',
    AudioGuidanceType.BEFORE_TASK_EXECUTION: 'before_task_audio',
    AudioGuidanceType.AFTER_TASK_EXECUTION: 'after_task_audio',
    AudioGuidanceType.BEFORE_QUESTION_EXECUTION: 'before_question_audio',
    AudioGuidanceType.AFTER_QUESTION_EXECUTION: 'after_question_audio',
    AudioGuidanceType.START_INTERVIEW: 'start_interview_audio',
    AudioGuidanceType.END_INTERVIEW: 'end_interview_audio',
}

TASK_TYPE_TEMPLATE_MAPPER = {
    TaskType.SPEAKING: 'tasks/speaking.html',
    TaskType.STUDY_THE_ADVERTISEMENT: 'tasks/study_the_advertisement.html',
    TaskType.INTERVIEW: 'tasks/interview.html',
    TaskType.IMAGE_SPEAKING: 'tasks/image_speaking.html',
}

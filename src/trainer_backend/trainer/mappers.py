from .enums import AudioGuidanceType
from .enums import TaskType


AudioGuidanceFieldMapper = {
    AudioGuidanceType.START_EXAM: 'begin_audio_guidance',
    AudioGuidanceType.END_EXAM: 'end_audio_guidance',
    AudioGuidanceType.BEFORE_TASK_EXECUTION: 'audio_before_execution',
    AudioGuidanceType.INTERVIEW_END: 'audio_after_execution'
}

TaskTypeTemplateMapper = {
    TaskType.SPEAKING: 'tasks/speaking.html',
    TaskType.STUDY_THE_ADVERTISEMENT: 'tasks/study_the_advertisement.html',
    TaskType.INTERVIEW: 'tasks/interview.html',
    TaskType.IMAGE_SPEAKING: 'tasks/image_speaking.html',
}

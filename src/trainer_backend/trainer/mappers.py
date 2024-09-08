from .enums import AudioGuidanceType


AudioGuidanceFieldMapper = {
    AudioGuidanceType.START_EXAM: 'begin_audio_guidance',
    AudioGuidanceType.END_EXAM: 'end_audio_guidance',
    AudioGuidanceType.BEFORE_TASK_EXECUTION: 'audio_before_execution',
    AudioGuidanceType.INTERVIEW_END: 'audio_after_execution'
}

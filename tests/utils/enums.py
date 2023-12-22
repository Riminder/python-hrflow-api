from enum import Enum


class TAGGING_ALGORITHM(str, Enum):
    TAGGER_ROME_FAMILY = "tagger-rome-family"
    TAGGER_ROME_SUBFAMILY = "tagger-rome-subfamily"
    TAGGER_ROME_CATEGORY = "tagger-rome-category"
    TAGGER_ROME_JOBTITLE = "tagger-rome-jobtitle"
    TAGGER_HRFLOW_SKILLS = "tagger-hrflow-skills"
    TAGGER_HRFLOW_LABELS = "tagger-hrflow-labels"


class PERMISSION(str, Enum):
    ALL = "all"
    WRITE = "write"
    READ = "read"

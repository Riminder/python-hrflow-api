import typing as t

from ..schemas import Education, Experience, HrFlowProfile
from .searching import is_valid_for_searching


def is_valid_experiences_for_scoring(
    experience_list: t.Optional[t.List[Experience]],
) -> bool:
    """
    Check if a list of experiences is valid for scoring

    Args:
        experience_list:        <list>
                                List of experiences to check
    Return:
        <bool>                  True if the list of experiences is valid for
                                scoring, False otherwise
    """
    for experience in experience_list:
        if experience.title:
            return True

    return False


def is_valid_educations_for_scoring(
    education_list: t.Optional[t.List[Education]],
) -> bool:
    """
    Check if a list of educations is valid for scoring

    Args:
        education_list:         <list>
                                List of educations to check
    Return:
        <bool>                  True if the list of educations is valid for
                                scoring, False otherwise
    """
    for education in education_list:
        if education.title or education.school:
            return True
    return False


def is_valid_for_scoring(
    profile: t.Union[t.Dict, HrFlowProfile],
) -> bool:
    """
    Check if a profile is valid for scoring

    Based on the following schemas https://developers.hrflow.ai/docs/profiles-scoring

    Args:
        client:                 <Hrflow>
                                Hrflow client
        profile:                <dict> or <HrFlowProfile>
                                Profile to check
    Return:
        <bool>                  True if the profile is valid for scoring,
                                False otherwise
    """
    if isinstance(profile, dict):
        profile = HrFlowProfile.parse_obj(profile)

    if not isinstance(profile, HrFlowProfile):
        raise ValueError("profile must be a dict or a HrFlowProfile object")

    return is_valid_for_searching(profile) and (
        is_valid_experiences_for_scoring(profile.experiences)
        or is_valid_educations_for_scoring(profile.educations)
        or bool(profile.info.summary)
        or bool(profile.skills)
        or bool(profile.tasks)
    )

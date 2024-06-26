import typing as t

from ..hrflow import Hrflow
from ..schemas import Education, Experience, HrFlowProfile


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
    for education in education_list:
        if education.title or education.school:
            return True
    return False


def is_valid_for_scoring(
    client: Hrflow,
    profile: t.Optional[t.Union[t.Dict, HrFlowProfile]] = None,
    source_key: t.Optional[str] = None,
    profile_key: t.Optional[str] = None,
    profile_reference: t.Optional[str] = None,
) -> bool:
    """
    Check if a profile is valid for scoring

    Based on the following schemas https://developers.hrflow.ai/docs/profiles-scoring

    Args:
        client:                 <Hrflow>
                                Hrflow client
        profile:                <dict> or <HrFlowProfile>
                                Profile to check. Can be not provided if source_key,
                                profile_key or profile_reference are provided
        source_key:             <str>
                                Source key. If provided, profile_key or
                                profile_reference must be also provided.
        profile_key:            <str>
                                Profile key. If provided, profile_reference must be None
        profile_reference:      <str>
                                Profile reference. If provided, profile_key must be None
    Return:
        <bool>                  True if the profile is valid for scoring,
                                False otherwise
    """
    # Check parameters and fetch profile if needed
    if profile is None:
        if source_key is None:
            raise ValueError("profile or source_key must be provided")
        elif profile_key is None and profile_reference is None:
            raise ValueError("profile_key or profile_reference must be provided")

        response = client.profile.storing.get(
            source_key=source_key, key=profile_key, reference=profile_reference
        )
        if response["code"] >= 400:
            message = response["message"]
            raise ValueError(f"Error while fetching profile: {message}")
        profile = response["data"]
    else:
        if (
            source_key is not None
            or profile_key is not None
            or profile_reference is not None
        ):

            raise ValueError(
                "If you provide a profile, you can't provide source_key, profile_key "
                "or profile_reference"
            )

    if isinstance(profile, dict):
        profile = HrFlowProfile.parse_obj(profile)

    if not isinstance(profile, HrFlowProfile):
        raise ValueError("profile must be a dict or a HrFlowProfile object")

    # Check if profile is valid for scoring
    return (
        is_valid_experiences_for_scoring(profile.experiences)
        or is_valid_educations_for_scoring(profile.educations)
        or bool(profile.summary)
        or bool(profile.skills)
        or bool(profile.tasks)
    )

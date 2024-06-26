import typing as t

from ..schemas import HrFlowProfile, ProfileInfo


def is_valid_info_for_searching(info: ProfileInfo) -> bool:
    """
    Check if the info part of a profile is valid for searching

    Based on the following schemas https://developers.hrflow.ai/docs/profiles-searching

    Args:
        info:                   <ProfileInfo>
                                Info part of the profile
    """
    if not isinstance(info, ProfileInfo):
        raise ValueError("info must be a ProfileInfo object")

    first_name_score = 1 if info.first_name else 0
    last_name_score = 1 if info.last_name else 0
    phone_score = 1 if info.phone else 0
    date_birth_score = 1 if info.date_birth else 0
    gender_score = 1 if info.gender else 0
    summary_score = 1 if info.summary else 0
    urls_score = 1 if info.urls else 0
    location_score = 1 if info.location else 0

    info_score = (
        first_name_score
        + last_name_score
        + phone_score
        + date_birth_score
        + gender_score
        + summary_score
        + urls_score
        + location_score
    )
    info_score = info_score / 8
    has_person = info.first_name and info.last_name

    return info.email or has_person or info_score >= 0.5


def is_valid_for_searching(
    profile: t.Union[t.Dict, HrFlowProfile],
) -> bool:
    """
    Check if a profile is valid for searching

    Based on the following schemas https://developers.hrflow.ai/docs/profiles-searching

    Args:
        client:                 <Hrflow>
                                Hrflow client
        profile:                <dict> or <HrFlowProfile>
                                Profile to check
    Return:
        <bool>                  True if the profile is valid for searching,
                                False otherwise
    """
    if isinstance(profile, dict):
        profile = HrFlowProfile.parse_obj(profile)

    if not isinstance(profile, HrFlowProfile):
        raise ValueError("profile must be a dict or a HrFlowProfile object")

    return is_valid_info_for_searching(profile.info) and bool(profile.text)

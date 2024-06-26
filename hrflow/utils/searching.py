import typing as t

from ..hrflow import Hrflow
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
    client: Hrflow,
    profile: t.Optional[t.Union[t.Dict, HrFlowProfile]] = None,
    source_key: t.Optional[str] = None,
    profile_key: t.Optional[str] = None,
    profile_reference: t.Optional[str] = None,
) -> bool:
    """
    Check if a profile is valid for searching

    Based on the following schemas https://developers.hrflow.ai/docs/profiles-searching

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
        <bool>                  True if the profile is valid for searching,
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

    # Check if profile is valid for searching
    return is_valid_info_for_searching(profile.info) and bool(profile.text)

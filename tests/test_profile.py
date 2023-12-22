import json
import typing as t
from time import sleep
from uuid import uuid4

import pytest
from requests import codes as http_codes

from hrflow import Hrflow

from .utils.schemas import (
    ProfileArchiveResponse,
    ProfileAskingResponse,
    ProfileIndexingResponse,
    ProfileParsingFileResponse,
    ProfilesScoringResponse,
    ProfilesSearchingResponse,
    ProfileUnfoldingResponse,
)
from .utils.tools import (
    _check_same_keys_equality,
    _file_get,
    _indexed_response_get,
    _now_iso8601_get,
    _var_from_env_get,
)

_MAX_RETRIES = 5
_ASYNC_RETRY_INTERVAL_SECONDS = 5
_ASYNC_TIMEOUT_SECONDS = 60


def _profile_get() -> t.Dict[str, t.Any]:
    return dict(
        reference=str(uuid4()),
        text_language="en",
        text=(
            "Harry James PotterSorcerer Apprenticedate of birth: June 26th 1997Number"
            " 4, Privet Drive, Little Whingingemail: harry.potter@hogwarts.netphone:"
            " 0747532699ExperiencesApril 2002 - July 2002	Hogwarts School of Witchcraft"
            " and WizardryMagic InvestigatorSolving mysteries about the Sorcerer's"
            " stone.teamplayer, empathy.EducationsDecember 2001 - December"
            " 2002	Hogwarts"
            " School of Witchcraft and WizardrySorcerer ApprenticeFirst year of"
            " study.witchcraft, levitation, lycanthropy.Skillswitchcraftdark"
            " artsperseveranceempathyInterestsquidditchwizard chess"
        ),
        created_at=_now_iso8601_get(),
        info=dict(
            full_name="Harry James Potter",
            first_name="Harry James",
            last_name="Potter",
            email="harry.potter@hogwarts.net",
            phone="0747532699",
            driving_license="Class B",
            date_birth="1997-06-26T00:00:00+0000",
            location=dict(text="Hogwarts", lat=12.345678, lng=-87.654321),
            urls=[dict(type="github", url="https://github.com/Riminder")],
            picture="https://path.to/picture",
            summary="Sorcerer Apprentice",
            gender="male",
        ),
        experiences_duration=0.2493150684931507,
        educations_duration=1.0,
        experiences=[
            dict(
                company="Hogwarts School of Witchcraft and Wizardry",
                title="Magic Investigator",
                description="Solving mysteries about the Sorcerer's stone.",
                location=dict(text="Hogwarts", lat=12.345678, lng=-87.654321),
                logo="https://path.to/logo",
                # The experience date string must not end with +0000
                # Ideally, it should follow the format yyyy-mm-ddTHH:MM:SS
                date_start="2002-04-01T00:00:00",
                date_end="2002-07-01T00:00:00",
                skills=[dict(name="Teamplayer", type="hard", value="90/100")],
                certifications=[dict(name="Wizardry", value="Individual")],
                courses=[dict(name="Advanced Potion-Making", value="On campus")],
                tasks=[dict(name="Defeat the Basilisk", value="Bravery")],
                languages=[dict(name="English", value="Fluent")],
                interests=[dict(name="Levitation", value="Amateur")],
            )
        ],
        educations=[
            dict(
                school="Hogwarts School of Witchcraft and Wizardry",
                title="Sorcerer Apprentice",
                description="First year of study.",
                location=dict(text="Hogwarts", lat=12.345678, lng=-87.654321),
                logo="https://path.to/logo",
                date_start="2001-12-01T00:00:00+0000",
                date_end="2002-12-01T00:00:00+0000",
                skills=[dict(name="Levitation", type="hard", value="88/100")],
                certifications=[dict(name="Wizardry", value="Individual")],
                courses=[dict(name="Advanced Potion-Making", value="On campus")],
                tasks=[dict(name="Defeat the Basilisk", value="Bravery")],
                interests=[dict(name="Levitation", value="Amateur")],
                languages=[dict(name="English", value="Fluent")],
            )
        ],
        skills=[dict(name="Lycanthropy", type="hard", value="93/100")],
        languages=[dict(name="English", value="Native")],
        certifications=[dict(name="Wizardry", value="Individual")],
        courses=[dict(name="Advanced Potion-Making", value="On campus")],
        tasks=[dict(name="Defeat the Basilisk", value="Bravery")],
        interests=[dict(name="Levitation", value="Amateur")],
        tags=[dict(name="Brave", value="1")],
        metadatas=[
            dict(
                name="Defeat the Basilisk",
                value=(
                    "To defeat the Basilisk, a few key elements: a weapon, courage and"
                    " determination, quick reflexes and support."
                ),
            )
        ],
    )


@pytest.mark.profile
@pytest.mark.parsing_file_sync
@pytest.mark.quicksilver
def test_profile_parsing_file_quicksilver_sync_basic():
    s3_url = """https://riminder-documents-eu-2019-12.s3-eu-west-1.amazonaws.com/\
teams/fc9d40fd60e679119130ea74ae1d34a3e22174f2/sources/07065e555609a231752a586afd6\
495c951bbae6b/profiles/1fed6e15b2df4465b1e406adabd0075d3214bc18/parsing/resume.pdf"""
    file = _file_get(s3_url, "profile_sync")
    model = ProfileParsingFileResponse.model_validate(
        Hrflow(
            api_secret=_var_from_env_get("HRFLOW_API_KEY"),
            api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
        ).profile.parsing.add_file(
            source_key=_var_from_env_get("HRFLOW_SOURCE_KEY_QUICKSILVER_SYNC"),
            profile_file=file,
        )
    )
    assert model.code == http_codes.created
    assert model.data.profile
    profile = model.data.profile.model_dump()
    if profile.get("info"):
        info = profile["info"]
        full_name_lower = info["full_name"].lower()
        assert "nico" in full_name_lower and "durant" in full_name_lower
        assert "nico" in info["first_name"].lower()
        assert "durant" in info["last_name"].lower()
        assert info["phone"] == "+33631245722"
        assert info["driving_license"] == "B"
        assert info["email"] == "exempledecv@cvmaker.com"
    if profile.get("languages"):
        languages_str_lower = json.dumps(profile["languages"]).lower()
        assert (
            "espagnol" in languages_str_lower
            or "allemand" in languages_str_lower
            or "anglais" in languages_str_lower
        )
    if profile.get("skills"):
        skills_str_lower = json.dumps(profile["skills"]).lower()
        assert (
            "word" in skills_str_lower
            or "excel" in skills_str_lower
            or "power point" in skills_str_lower
            or "photoshop" in skills_str_lower
        )
    if profile.get("educations"):
        educations_str_lower = json.dumps(
            profile["educations"], ensure_ascii=False
        ).lower()
        assert "ecole de commerce" in educations_str_lower
        assert (
            "comptabilité" in educations_str_lower or "gestion" in educations_str_lower
        )
        assert (
            "audit" in educations_str_lower
            or "droit des affaires" in educations_str_lower
        )
        assert "baccalauréat général économique" in educations_str_lower
        assert "lycée" in educations_str_lower
        assert "paris" in educations_str_lower
        assert "bureau des étudiants" in educations_str_lower
    if profile.get("experiences"):
        experiences_str_lower = json.dumps(
            profile["experiences"], ensure_ascii=False
        ).lower()
        assert "paris" in experiences_str_lower
        assert (
            "vendeur" in experiences_str_lower
            or "sport magasin" in experiences_str_lower
        )
        assert (
            "accueil des clients" in experiences_str_lower
            or "gestion du stock" in experiences_str_lower
            or "gestion de la caisse" in experiences_str_lower
            or "rangement du stock" in experiences_str_lower
        )
        assert "animateur" in experiences_str_lower
        assert (
            "accueil des vacanciers" in experiences_str_lower
            or "animation d'ateliers pour les jeunes de 8 à 10 ans"
            in experiences_str_lower
            or "soutien administratif" in experiences_str_lower
        )
        assert (
            "camping sable & me" in experiences_str_lower
            or "juan-les-bains" in experiences_str_lower
        )
        assert "baby-sitting" in experiences_str_lower
        assert (
            "garde d'enfants âgés de 5 ans et 7 ans" in experiences_str_lower
            or "sortie d'école" in experiences_str_lower
            or "aide aux devoirs" in experiences_str_lower
            or "préparation de repas" in experiences_str_lower
            or "jeux éducatifs" in experiences_str_lower
        )


@pytest.mark.profile
@pytest.mark.parsing_file_sync
@pytest.mark.hawk
def test_profile_parsing_file_hawk_sync_basic():
    s3_url = """https://riminder-documents-eu-2019-12.s3-eu-west-1.amazonaws.com/\
teams/fc9d40fd60e679119130ea74ae1d34a3e22174f2/sources/07065e555609a231752a586afd6\
495c951bbae6b/profiles/1fed6e15b2df4465b1e406adabd0075d3214bc18/parsing/resume.pdf"""
    file = _file_get(s3_url, "profile_sync")
    model = ProfileParsingFileResponse.model_validate(
        Hrflow(
            api_secret=_var_from_env_get("HRFLOW_API_KEY"),
            api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
        ).profile.parsing.add_file(
            source_key=_var_from_env_get("HRFLOW_SOURCE_KEY_HAWK_SYNC"),
            profile_file=file,
        )
    )
    assert model.code == http_codes.created
    assert model.data.profile
    profile = model.data.profile.model_dump()
    if profile.get("info"):
        info = profile["info"]
        full_name_lower = info["full_name"].lower()
        assert "nico" in full_name_lower and "durant" in full_name_lower
        assert "nico" in info["first_name"].lower()
        assert "durant" in info["last_name"].lower()
        assert info["phone"] == "+33631245722"
        assert info["driving_license"] == "B"
        assert info["email"] == "exempledecv@cvmaker.com"
    if profile.get("languages"):
        languages_str_lower = json.dumps(profile["languages"]).lower()
        assert (
            "espagnol" in languages_str_lower
            or "allemand" in languages_str_lower
            or "anglais" in languages_str_lower
        )
    if profile.get("skills"):
        skills_str_lower = json.dumps(profile["skills"]).lower()
        assert (
            "word" in skills_str_lower
            or "excel" in skills_str_lower
            or "power point" in skills_str_lower
            or "photoshop" in skills_str_lower
        )
    if profile.get("educations"):
        educations_str_lower = json.dumps(
            profile["educations"], ensure_ascii=False
        ).lower()
        assert "ecole de commerce" in educations_str_lower
        assert (
            "comptabilité" in educations_str_lower or "gestion" in educations_str_lower
        )
        assert (
            "audit" in educations_str_lower
            or "droit des affaires" in educations_str_lower
        )
        assert "baccalauréat général économique" in educations_str_lower
        assert "lycée" in educations_str_lower
        assert "paris" in educations_str_lower
        assert "bureau des étudiants" in educations_str_lower
    if profile.get("experiences"):
        experiences_str_lower = json.dumps(
            profile["experiences"], ensure_ascii=False
        ).lower()
        assert "paris" in experiences_str_lower
        assert (
            "vendeur" in experiences_str_lower
            or "sport magasin" in experiences_str_lower
        )
        assert (
            "accueil des clients" in experiences_str_lower
            or "gestion du stock" in experiences_str_lower
            or "gestion de la caisse" in experiences_str_lower
            or "rangement du stock" in experiences_str_lower
        )
        assert "animateur" in experiences_str_lower
        assert (
            "accueil des vacanciers" in experiences_str_lower
            or "animation d'ateliers pour les jeunes de 8 à 10 ans"
            in experiences_str_lower
            or "soutien administratif" in experiences_str_lower
        )
        assert (
            "camping sable & me" in experiences_str_lower
            or "juan-les-bains" in experiences_str_lower
        )
        assert "baby-sitting" in experiences_str_lower
        assert (
            "garde d'enfants âgés de 5 ans et 7 ans" in experiences_str_lower
            or "sortie d'école" in experiences_str_lower
            or "aide aux devoirs" in experiences_str_lower
            or "préparation de repas" in experiences_str_lower
            or "jeux éducatifs" in experiences_str_lower
        )


@pytest.mark.profile
@pytest.mark.parsing_file_async
@pytest.mark.quicksilver
def test_profile_parsing_file_quicksilver_async_basic():
    SOURCE_KEY = _var_from_env_get("HRFLOW_SOURCE_KEY_QUICKSILVER_ASYNC")
    s3_url = """https://riminder-documents-eu-2019-12.s3-eu-west-1.amazonaws.com/\
teams/fc9d40fd60e679119130ea74ae1d34a3e22174f2/sources/06d96aab2661b16eaf4d34d385d\
3c2b0cf00c0eb/profiles/d79768fb63013a8bdd04e7e8742cc84afd428a87/parsing/resume.pdf"""
    file = _file_get(s3_url, "profile_async")
    reference = str(uuid4())
    hf = Hrflow(
        api_secret=_var_from_env_get("HRFLOW_API_KEY"),
        api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
    )
    model = ProfileParsingFileResponse.model_validate(
        hf.profile.parsing.add_file(
            source_key=SOURCE_KEY,
            profile_file=file,
            reference=reference,
        )
    )
    assert model.code == http_codes.accepted
    assert _ASYNC_RETRY_INTERVAL_SECONDS > 0
    for _ in range(max(0, _ASYNC_TIMEOUT_SECONDS // _ASYNC_RETRY_INTERVAL_SECONDS)):
        model = ProfileIndexingResponse.model_validate(
            hf.profile.storing.get(source_key=SOURCE_KEY, reference=reference)
        )
        if model.code == http_codes.ok:
            break
        sleep(_ASYNC_RETRY_INTERVAL_SECONDS)
    assert model.code == http_codes.ok or pytest.fail(
        "failed to retrieve an asynchronously parsed profile with"
        f" timeout={_ASYNC_TIMEOUT_SECONDS} and"
        f" interval={_ASYNC_RETRY_INTERVAL_SECONDS}"
    )
    assert model.data is not None
    profile = model.data.model_dump()
    assert "john" in profile["info"]["full_name"].lower()
    assert "john@smith.com" in profile["info"]["email"].lower()
    assert profile["info"]["phone"].count("5") >= 9
    location_text_lower = profile["info"]["location"]["text"].lower()
    assert (
        "141 highway street road" in location_text_lower
        or "scottsdale" in location_text_lower
        or "hawaii" in location_text_lower
    )
    skills_str_lower = json.dumps(profile["skills"]).lower()
    assert (
        "web development" in skills_str_lower
        or "adobe photoshop" in skills_str_lower
        or "adobe dreamweaver" in skills_str_lower
        or "indesign" in skills_str_lower
        or "illustrator" in skills_str_lower
        or "after effects" in skills_str_lower
        or "css" in skills_str_lower
        or "javascript" in skills_str_lower
        or "responsive web design" in skills_str_lower
        or "php" in skills_str_lower
        or "jquery" in skills_str_lower
        or "wordpress" in skills_str_lower
        or "cmd/sharepoint" in skills_str_lower
        or "animated gifs" in skills_str_lower
        or "web banners" in skills_str_lower
        or "project management" in skills_str_lower
        or "technical writing" in skills_str_lower
        or "seo" in skills_str_lower
    )
    educations_str_lower = json.dumps(profile["educations"]).lower()
    assert (
        "masters of information systems" in educations_str_lower
        or "bachelors of science" in educations_str_lower
    )
    experiences_str_lower = json.dumps(profile["experiences"]).lower()
    assert "web designer intern" in experiences_str_lower
    assert "scottsdale, hawaii" in experiences_str_lower
    assert (
        "html" in experiences_str_lower
        or "css" in experiences_str_lower
        or "jquery" in experiences_str_lower
    )


@pytest.mark.profile
@pytest.mark.parsing_file_async
@pytest.mark.mozart
def test_profile_parsing_file_mozart_async_basic():
    SOURCE_KEY = _var_from_env_get("HRFLOW_SOURCE_KEY_MOZART_ASYNC")
    s3_url = """https://riminder-documents-eu-2019-12.s3-eu-west-1.amazonaws.com/\
teams/fc9d40fd60e679119130ea74ae1d34a3e22174f2/sources/06d96aab2661b16eaf4d34d385d\
3c2b0cf00c0eb/profiles/d79768fb63013a8bdd04e7e8742cc84afd428a87/parsing/resume.pdf"""
    file = _file_get(s3_url, "profile_async")
    reference = str(uuid4())
    hf = Hrflow(
        api_secret=_var_from_env_get("HRFLOW_API_KEY"),
        api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
    )
    model = ProfileParsingFileResponse.model_validate(
        hf.profile.parsing.add_file(
            source_key=SOURCE_KEY,
            profile_file=file,
            reference=reference,
        )
    )
    assert model.code == http_codes.accepted
    assert _ASYNC_RETRY_INTERVAL_SECONDS > 0
    for _ in range(max(0, _ASYNC_TIMEOUT_SECONDS // _ASYNC_RETRY_INTERVAL_SECONDS)):
        model = ProfileIndexingResponse.model_validate(
            hf.profile.storing.get(source_key=SOURCE_KEY, reference=reference)
        )
        if model.code == http_codes.ok:
            break
        sleep(_ASYNC_RETRY_INTERVAL_SECONDS)
    assert model.code == http_codes.ok or pytest.fail(
        "failed to retrieve an asynchronously parsed profile with"
        f" timeout={_ASYNC_TIMEOUT_SECONDS} and"
        f" interval={_ASYNC_RETRY_INTERVAL_SECONDS}"
    )
    assert model.data is not None
    profile = model.data.model_dump()
    assert "john" in profile["info"]["full_name"].lower()
    assert "john@smith.com" in profile["info"]["email"].lower()
    assert profile["info"]["phone"].count("5") >= 9
    location_text_lower = profile["info"]["location"]["text"].lower()
    assert (
        "141 highway street road" in location_text_lower
        or "scottsdale" in location_text_lower
        or "hawaii" in location_text_lower
    )
    skills_str_lower = json.dumps(profile["skills"]).lower()
    assert (
        "web development" in skills_str_lower
        or "adobe photoshop" in skills_str_lower
        or "adobe dreamweaver" in skills_str_lower
        or "indesign" in skills_str_lower
        or "illustrator" in skills_str_lower
        or "after effects" in skills_str_lower
        or "css" in skills_str_lower
        or "javascript" in skills_str_lower
        or "responsive web design" in skills_str_lower
        or "php" in skills_str_lower
        or "jquery" in skills_str_lower
        or "wordpress" in skills_str_lower
        or "cmd/sharepoint" in skills_str_lower
        or "animated gifs" in skills_str_lower
        or "web banners" in skills_str_lower
        or "project management" in skills_str_lower
        or "technical writing" in skills_str_lower
        or "seo" in skills_str_lower
    )
    educations_str_lower = json.dumps(profile["educations"]).lower()
    assert (
        "masters of information systems" in educations_str_lower
        or "bachelors of science" in educations_str_lower
    )
    experiences_str_lower = json.dumps(profile["experiences"]).lower()
    assert "web designer intern" in experiences_str_lower
    assert "scottsdale, hawaii" in experiences_str_lower
    assert (
        "html" in experiences_str_lower
        or "css" in experiences_str_lower
        or "jquery" in experiences_str_lower
    )


@pytest.mark.profile
@pytest.mark.indexing
def test_profile_indexing_basic():
    profile = _profile_get()
    model = ProfileIndexingResponse.model_validate(
        Hrflow(
            api_secret=_var_from_env_get("HRFLOW_API_KEY"),
            api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
        ).profile.storing.add_json(
            source_key=_var_from_env_get("HRFLOW_SOURCE_KEY_QUICKSILVER_SYNC"),
            profile_json=profile,
        )
    )
    assert model.code == http_codes.created
    assert model.data is not None
    _check_same_keys_equality(profile, model.data)


@pytest.mark.profile
@pytest.mark.searching
def test_profiles_searching_basic():
    model = ProfilesSearchingResponse.model_validate(
        Hrflow(
            api_secret=_var_from_env_get("HRFLOW_API_KEY"),
            api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
        ).profile.searching.list(
            source_keys=[_var_from_env_get("HRFLOW_SOURCE_KEY_QUICKSILVER_SYNC")],
            limit=5,  # allows to bypass the bug with archived profiles
        )
    )
    assert model.code == http_codes.ok


@pytest.mark.profile
@pytest.mark.scoring
def test_profiles_scoring_basic():
    model = ProfilesScoringResponse.model_validate(
        Hrflow(
            api_secret=_var_from_env_get("HRFLOW_API_KEY"),
            api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
        ).profile.scoring.list(
            algorithm_key=_var_from_env_get("HRFLOW_ALGORITHM_KEY"),
            board_key=_var_from_env_get("HRFLOW_BOARD_KEY"),
            source_keys=[_var_from_env_get("HRFLOW_SOURCE_KEY_QUICKSILVER_SYNC")],
            job_key=_var_from_env_get("HRFLOW_JOB_KEY"),
            limit=5,  # allows to bypass the bug with archived profiles
        )
    )
    assert model.code == http_codes.ok


@pytest.mark.profile
@pytest.mark.asking
def test_profile_asking_basic():
    hf = Hrflow(
        api_secret=_var_from_env_get("HRFLOW_API_KEY"),
        api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
    )
    SOURCE_KEY = _var_from_env_get("HRFLOW_SOURCE_KEY_QUICKSILVER_SYNC")
    model = ProfileAskingResponse.model_validate(
        hf.profile.asking.get(
            source_key=SOURCE_KEY,
            key=_indexed_response_get(hf, SOURCE_KEY, _profile_get()).data.key,
            questions=[
                "What is the full name of the profile ?",
            ],
        )
    )
    assert model.code == http_codes.ok
    assert len(model.data) == 1
    assert "harry james potter" in model.data[0].lower()


@pytest.mark.skip(reason="backend: multiple questions are not correctly handled yet")
@pytest.mark.profile
@pytest.mark.asking
def test_profile_asking_multiple_questions():
    hf = Hrflow(
        api_secret=_var_from_env_get("HRFLOW_API_KEY"),
        api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
    )
    SOURCE_KEY = _var_from_env_get("HRFLOW_SOURCE_KEY_QUICKSILVER_SYNC")
    questions = [
        "What is the full name of the profile ?",
        "Does the applicant have a driver's licence ?",
        "What year did the profile finish school ?",
    ]
    model = ProfileAskingResponse.model_validate(
        hf.profile.asking.get(
            source_key=SOURCE_KEY,
            questions=questions,
            key=_indexed_response_get(hf, SOURCE_KEY, _profile_get()).data.key,
        )
    )
    assert model.code == http_codes.ok
    assert len(model.data) == len(questions)
    assert "harry james potter" in model.data[0].lower()
    assert "yes" in model.data[0].lower()
    assert "2002" in model.data[2]


@pytest.mark.profile
@pytest.mark.asking
def test_profile_asking_no_question():
    hf = Hrflow(
        api_secret=_var_from_env_get("HRFLOW_API_KEY"),
        api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
    )
    SOURCE_KEY = _var_from_env_get("HRFLOW_SOURCE_KEY_QUICKSILVER_SYNC")
    model = ProfileAskingResponse.model_validate(
        hf.profile.asking.get(
            source_key=SOURCE_KEY,
            key=_indexed_response_get(hf, SOURCE_KEY, _profile_get()).data.key,
            questions=None,
        )
    )
    assert model.code == http_codes.bad_request


@pytest.mark.profile
@pytest.mark.unfolding
def test_profile_unfolding_basic():
    hf = Hrflow(
        api_secret=_var_from_env_get("HRFLOW_API_KEY"),
        api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
    )
    SOURCE_KEY = _var_from_env_get("HRFLOW_SOURCE_KEY_QUICKSILVER_SYNC")
    profile = _profile_get()
    if profile.get("experiences") and len(profile["experiences"]) == 1:
        profile["experiences"].append(profile["experiences"][0].copy())  # shallow copy
        last_experience = profile["experiences"][-1]
        for dkey in ["date_start", "date_end"]:
            datestr = last_experience.get(dkey)
            if datestr is not None:  # +1 year
                last_experience[dkey] = str(int(datestr[:4]) + 1) + datestr[4:]
    for _ in range(_MAX_RETRIES):
        model = ProfileUnfoldingResponse.model_validate(
            hf.profile.unfolding.get(
                source_key=SOURCE_KEY,
                key=_indexed_response_get(hf, SOURCE_KEY, profile).data.key,
            )
        )
        if model.code != http_codes.server_error:
            break
    assert model.code == http_codes.ok
    assert len(model.data.experiences) == 1


@pytest.mark.profile
@pytest.mark.unfolding
def test_profile_unfolding_no_experience():
    hf = Hrflow(
        api_secret=_var_from_env_get("HRFLOW_API_KEY"),
        api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
    )
    SOURCE_KEY = _var_from_env_get("HRFLOW_SOURCE_KEY_QUICKSILVER_SYNC")
    profile = _profile_get()
    profile["experiences"] = list()
    model = ProfileUnfoldingResponse.model_validate(
        hf.profile.unfolding.get(
            source_key=SOURCE_KEY,
            key=_indexed_response_get(hf, SOURCE_KEY, profile).data.key,
        )
    )
    assert model.code == http_codes.bad_request


@pytest.mark.profile
@pytest.mark.archive
def test_profile_archive_basic():
    hf = Hrflow(
        api_secret=_var_from_env_get("HRFLOW_API_KEY"),
        api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
    )
    SOURCE_KEY = _var_from_env_get("HRFLOW_SOURCE_KEY_QUICKSILVER_SYNC")
    mock_key = _indexed_response_get(hf, SOURCE_KEY, _profile_get()).data.key
    model = ProfileArchiveResponse.model_validate(
        hf.profile.storing.archive(source_key=SOURCE_KEY, key=mock_key)
    )
    assert model.code == http_codes.ok
    assert model.data.key == mock_key


@pytest.mark.profile
@pytest.mark.editing
def test_profile_editing_basic():
    SOURCE_KEY = _var_from_env_get("HRFLOW_SOURCE_KEY_QUICKSILVER_SYNC")
    hf = Hrflow(
        api_secret=_var_from_env_get("HRFLOW_API_KEY"),
        api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
    )
    mock_profile = _indexed_response_get(hf, SOURCE_KEY, _profile_get()).data
    mock_profile.text = f"The password of my bitcoin wallet is {uuid4()}."
    model = ProfileIndexingResponse.model_validate(
        hf.profile.storing.edit(
            source_key=SOURCE_KEY,
            profile_json=mock_profile.model_dump(),
        )
    )
    assert model.code == http_codes.ok
    assert model.data.text == mock_profile.text

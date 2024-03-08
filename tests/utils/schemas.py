import typing as t
from math import ceil

from pydantic import (
    BaseModel,
    confloat,
    conint,
    conlist,
    constr,
    field_validator,
    model_validator,
)
from pytest import fail

from hrflow.utils import KEY_REGEX

from .enums import PERMISSION


class HrFlowAPIResponse(BaseModel):
    code: conint(ge=100, le=599)
    message: str
    model_config: t.Dict = dict(validate_assignment=True)


class Pagination(BaseModel):
    page: conint(ge=0)
    maxPage: conint(ge=0)
    count: conint(ge=0)
    total: conint(ge=0)

    @model_validator(mode="before")
    @classmethod
    def _check(cls, values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        page = values.get("page")
        max_page = values.get("maxPage")
        count = values.get("count")
        total = values.get("total")
        per_page = total / max_page

        assert page <= max_page

        if page == max_page:
            assert count <= per_page
        else:
            assert ceil(total / count) == max_page
            assert count >= per_page

        return values


class HrFlowAPIResponseWithPagination(HrFlowAPIResponse):
    meta: Pagination


# Text API


class TextImagingData(BaseModel):
    image_url: str


class TextImagingResponse(HrFlowAPIResponse):
    data: t.Optional[TextImagingData] = None


class TextEmbeddingDataItem(BaseModel):
    embedding: conlist(float, min_length=2048, max_length=2048)


class TextEmbeddingResponse(HrFlowAPIResponse):
    data: t.Optional[t.List[TextEmbeddingDataItem]] = None


_LINKING_DATA_ITEM_TYPE = conlist(t.Any, min_length=2, max_length=2)
_LINKING_DATA_TYPE = t.List[_LINKING_DATA_ITEM_TYPE]


class TextLinkingResponse(HrFlowAPIResponse):
    data: t.Optional[_LINKING_DATA_TYPE] = None

    @field_validator("data")
    @classmethod
    def _check_data(cls, data: _LINKING_DATA_TYPE) -> _LINKING_DATA_TYPE:
        assert all(
            isinstance(item[0], str)
            and isinstance(item[1], (int, float))
            and item[1] >= 0
            and item[1] <= 1
            for item in data
        )
        return data


class TextTaggingDataItem(BaseModel):
    ids: t.List[str]
    predictions: t.List[float]
    tags: t.List[str]

    @model_validator(mode="before")
    @classmethod
    def _check(cls, values: t.Dict[str, t.List[t.Any]]) -> t.Dict[str, t.List[t.Any]]:
        if isinstance(values, list):
            return [cls._check(item) for item in values]
        li = len(values.get("ids"))
        lp = len(values.get("predictions"))
        lt = len(values.get("tags"))
        assert li == lp == lt or fail(
            f"len(ids)={li} is expected to be same as len(predictions)={lp} and same as"
            f" len(tags)={lt}"
        )
        return values


class TextTaggingReponse(HrFlowAPIResponse):
    data: t.Optional[t.Union[t.List[TextTaggingDataItem], TextTaggingDataItem]] = None


class TextParsingDataItemEntity(BaseModel):
    start: conint(ge=0)
    end: conint(ge=0)
    label: str

    @model_validator(mode="before")
    @classmethod
    def _check(cls, values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        start = values.get("start")
        end = values.get("end")
        assert start <= end or fail(f"{start=} is expected to be smaller than {end=}")
        return values


class TextParsingDataItemParsing(BaseModel):
    certifications: t.List[str]
    companies: t.List[str]
    courses: t.List[str]
    dates: t.List[str]
    durations: t.List[str]
    education_titles: t.List[str]
    emails: t.List[str]
    first_names: t.List[str]
    interests: t.List[str]
    job_titles: t.List[str]
    languages: t.List[str]
    last_names: t.List[str]
    locations: t.List[str]
    phones: t.List[str]
    schools: t.List[str]
    skills_hard: t.List[str]
    skills_soft: t.List[str]
    tasks: t.List[str]


class TextParsingDataItem(BaseModel):
    entities: t.List[TextParsingDataItemEntity]
    parsing: TextParsingDataItemParsing
    text: str

    @model_validator(mode="before")
    @classmethod
    def _check(cls, values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        if isinstance(values, list):
            return [cls._check(item) for item in values]

        text = values.get("text")
        entities = values.get("entities")
        parsing = values.get("parsing")

        for entity in entities:
            parsing_key_name = entity["label"]

            # entity label to parsing object key name
            if parsing_key_name.startswith("skill"):
                parsing_key_name = "skills" + parsing_key_name[:5]
            elif parsing_key_name == "company":
                parsing_key_name = "companies"
            else:  # most of them
                parsing_key_name += "s"

            parsed = text[entity["start"] : entity["end"]]
            holder = parsing[parsing_key_name]

            assert parsed in holder or fail(f"{parsed=} is expected to be in {holder=}")

        return values


class TextParsingResponse(HrFlowAPIResponse):
    data: t.Optional[t.Union[TextParsingDataItem, t.List[TextParsingDataItem]]] = None


class TextOCRDataItemPage(BaseModel):
    page_number: conint(ge=0)
    sections: t.List[str]


_BASE64_PDF_TYPE = constr(pattern=r"^[A-Za-z0-9+/]*={0,2}$", strict=True)


class TextOCRDataItem(BaseModel):
    text_language: str
    text: str
    pages: t.List[TextOCRDataItemPage]
    base64_pdf: _BASE64_PDF_TYPE


class TextOCRResponse(HrFlowAPIResponse):
    data: t.Optional[TextOCRDataItem]


# Auth API


class AuthResponseData(BaseModel):
    team_name: str
    team_subdomain: str
    request_origin: t.Optional[str] = None
    api_key_permission: PERMISSION


class AuthResponse(HrFlowAPIResponse):
    data: t.Optional[AuthResponseData] = None


# HrFlow.ai object definitions


class Board(BaseModel):
    key: constr(pattern=KEY_REGEX)
    name: str
    type: str
    subtype: str
    environment: str


class Fields(BaseModel):
    category: t.Optional[str] = None
    city: t.Optional[str] = None
    city_district: t.Optional[str] = None
    country: t.Optional[str] = None
    country_region: t.Optional[str] = None
    entrance: t.Optional[str] = None
    house: t.Optional[str] = None
    house_number: t.Optional[str] = None
    island: t.Optional[str] = None
    level: t.Optional[str] = None
    near: t.Optional[str] = None
    po_box: t.Optional[str] = None
    postcode: t.Optional[str] = None
    road: t.Optional[str] = None
    staircase: t.Optional[str] = None
    state: t.Optional[str] = None
    state_district: t.Optional[str] = None
    suburb: t.Optional[str] = None
    text: t.Optional[str] = None
    unit: t.Optional[str] = None
    world_region: t.Optional[str] = None


class Location(BaseModel):
    text: t.Optional[str] = None
    lat: t.Optional[confloat(ge=-90, le=90)] = None
    lng: t.Optional[confloat(ge=-180, le=180)] = None
    gmaps: t.Optional[str] = None
    fields: t.Optional[
        t.Union[
            Fields,
            conlist(
                t.Any,
                min_length=0,
                max_length=0,
            ),
        ]
    ] = None


class Section(BaseModel):
    name: t.Optional[str] = None
    title: t.Optional[str] = None
    description: t.Optional[str] = None


class GeneralEntity(BaseModel):
    name: t.Optional[str] = None
    value: t.Optional[str] = None


class Skill(GeneralEntity):
    type: t.Optional[str] = None


class Language(GeneralEntity):
    pass


class Certification(GeneralEntity):
    pass


class Course(GeneralEntity):
    pass


class Task(GeneralEntity):
    pass


class Tag(GeneralEntity):
    pass


class Metadata(GeneralEntity):
    pass


class Interest(GeneralEntity):
    pass


class RangeFloat(BaseModel):
    name: t.Optional[str] = None
    value_min: t.Optional[float] = None
    value_max: t.Optional[float] = None
    unit: t.Optional[str] = None


class RangeDate(BaseModel):
    name: t.Optional[str] = None
    value_min: t.Optional[str] = None
    value_max: t.Optional[str] = None


class Job(BaseModel):
    id: conint(ge=0)
    key: t.Optional[constr(pattern=KEY_REGEX)] = None
    reference: t.Optional[str] = None
    board_key: str
    board: Board
    name: t.Optional[str] = None
    url: t.Optional[str] = None
    summary: t.Optional[str] = None
    location: t.Optional[Location] = None
    updated_at: t.Optional[str] = None
    created_at: t.Optional[str] = None
    sections: t.Optional[t.List[Section]] = None
    skills: t.Optional[t.List[Skill]] = None
    languages: t.Optional[t.List[Language]] = None
    certifications: t.Optional[t.List[Certification]] = None
    courses: t.Optional[t.List[Course]] = None
    tasks: t.Optional[t.List[Task]] = None
    tags: t.Optional[t.List[Tag]] = None
    metadatas: t.Optional[t.List[Metadata]] = None
    ranges_float: t.Optional[t.List[RangeFloat]] = None
    ranges_date: t.Optional[t.List[RangeDate]] = None
    culture: t.Optional[str] = None
    benefits: t.Optional[str] = None
    responsibilities: t.Optional[str] = None
    requirements: t.Optional[str] = None
    interviews: t.Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def _check(cls, values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        board_key = values.get("board_key")
        board = values.get("board")
        assert board_key == board["key"] or fail(
            f"{board_key=} is expected to be the same as {board['key']=}"
        )
        return values


class Source(Board):  # same fields
    pass


class Url(BaseModel):
    type: t.Optional[str] = None
    url: t.Optional[str] = None


class Info(BaseModel):
    full_name: t.Optional[str] = None
    first_name: t.Optional[str] = None
    last_name: t.Optional[str] = None
    email: t.Optional[str] = None
    phone: t.Optional[str] = None
    driving_license: t.Optional[str] = None
    date_birth: t.Optional[str] = None
    location: t.Optional[Location] = None
    urls: t.Optional[t.List[Url]] = None
    picture: t.Optional[str] = None
    gender: t.Optional[str] = None
    summary: t.Optional[str] = None


class E(BaseModel):
    key: t.Optional[constr(pattern=KEY_REGEX)] = None
    logo: t.Optional[str] = None
    title: t.Optional[str] = None
    description: t.Optional[str] = None
    location: t.Optional[Location] = None
    date_start: t.Optional[str] = None
    date_end: t.Optional[str] = None
    skills: t.Optional[t.List[Skill]] = None
    certifications: t.Optional[t.List[Certification]] = None
    courses: t.Optional[t.List[Course]] = None
    tasks: t.Optional[t.List[Task]] = None
    languages: t.Optional[t.List[Language]] = None
    interests: t.Optional[t.List[Interest]] = None


class Experience(E):
    company: t.Optional[str] = None


class Education(E):
    school: t.Optional[str] = None


class Attachment(BaseModel):
    type: t.Optional[str] = None
    alt: t.Optional[constr(pattern=KEY_REGEX)]
    file_size: t.Optional[conint(ge=0)] = None
    file_name: t.Optional[str] = None
    original_file_name: t.Optional[str] = None
    extension: t.Optional[str] = None
    public_url: t.Optional[str] = None
    updated_at: t.Optional[str] = None
    created_at: t.Optional[str] = None


class Profile(BaseModel):
    id: t.Optional[conint(ge=0)] = None
    key: t.Optional[constr(pattern=KEY_REGEX)] = None
    reference: t.Optional[str] = None
    source_key: str
    source: Source
    updated_at: t.Optional[str] = None
    created_at: t.Optional[str] = None
    info: t.Optional[Info] = None
    text_language: t.Optional[str] = None
    text: t.Optional[str] = None
    experiences_duration: t.Optional[confloat(ge=0)] = None
    educations_duration: t.Optional[confloat(ge=0)] = None
    experiences: t.Optional[t.List[Experience]] = None
    educations: t.Optional[t.List[Education]] = None
    skills: t.Optional[t.List[Skill]] = None
    languages: t.Optional[t.List[Language]] = None
    certifications: t.Optional[t.List[Certification]] = None
    courses: t.Optional[t.List[Course]] = None
    tasks: t.Optional[t.List[Task]] = None
    interests: t.Optional[t.List[Interest]] = None
    tags: t.Optional[t.List[Tag]] = None
    metadatas: t.Optional[t.List[Metadata]] = None

    @model_validator(mode="before")
    @classmethod
    def _check(cls, values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        source_key = values["source_key"]
        source = values["source"]
        assert source_key == source["key"] or fail(
            f"{source_key=} is expected to be the same as {source['key']=}"
        )
        return values


# Utils to factorise searching (or scoring) jobs (or profiles) responses


def _validate_searching_result(values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
    """
    Verifies if the returned number of jobs (or profiles) matches the value declared
    in the `meta.count` field.

    Args:
        values (dict): The dumped jobs (or profiles) searching response Pydantic
        object.

    Returns:
        The `values` if the response passes the test; otherwise, the test will be
        skipped.
    """

    expected = values["meta"]["count"]
    objects_key = "jobs" if "jobs" in values["data"] else "profiles"
    actual = len(values["data"][objects_key])

    assert actual == expected or fail(
        f"len(data.{objects_key})={actual} is expected to be same as"
        f" model.count={expected}"
    )

    return values


def _validate_scoring_result(values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
    """
    Verifies if the returned number of jobs (or profiles) AND predictions matches the
    value declared in the `meta.count` field.

    Args:
        values (dict): The dumped jobs (or profiles) scoring response Pydantic
        object.

    Returns:
        The `values` if the response passes the test; otherwise, the test will be
        skipped.
    """

    expected = values["meta"]["count"]
    predictions_amount = len(values["data"]["predictions"])
    objects_key = "jobs" if "jobs" in values["data"] else "profiles"
    objects_amount = len(values["data"][objects_key])

    assert objects_amount == predictions_amount == expected or fail(
        f"len(data.predictions)={predictions_amount} and"
        f" len(data.{objects_key})={objects_amount} are expected to be the same as"
        f" meta.count={expected}"
    )

    return values


# Job API


class JobIndexingResponse(HrFlowAPIResponse):
    data: t.Optional[Job]


class JobsSearchingData(BaseModel):
    jobs: t.List[Job]


class JobsSearchingResponse(HrFlowAPIResponseWithPagination):
    data: JobsSearchingData

    @model_validator(mode="before")
    @classmethod
    def _check(cls, values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        return _validate_searching_result(values)


class JobsScoringData(BaseModel):
    predictions: t.List[conlist(confloat(ge=0, le=1), min_length=2, max_length=2)]
    jobs: t.List[Job]


class JobsScoringResponse(HrFlowAPIResponseWithPagination):
    data: JobsScoringData

    @model_validator(mode="before")
    @classmethod
    def _check(cls, values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        return _validate_scoring_result(values)


class JobAskingResponse(HrFlowAPIResponse):
    data: t.Optional[t.List[str]] = None


class JobArchiveData(BaseModel):
    key: constr(pattern=KEY_REGEX)


class JobArchiveResponse(HrFlowAPIResponse):
    data: t.Optional[JobArchiveData] = None


# Profile API


class ProfileIndexingResponse(HrFlowAPIResponse):
    data: t.Optional[Profile] = None


class ProfileParsingFileDataItem(BaseModel):
    profile: t.Optional[Profile] = None


class ProfileParsingFileResponse(HrFlowAPIResponse):
    data: t.Optional[
        t.Union[
            ProfileParsingFileDataItem,
            conlist(  # for async
                t.Any,
                min_length=0,
                max_length=0,
            ),
        ]
    ] = None


class ProfilesSearchingData(BaseModel):
    profiles: t.List[Profile]


class ProfilesSearchingResponse(HrFlowAPIResponseWithPagination):
    data: ProfilesSearchingData

    @model_validator(mode="before")
    @classmethod
    def _check(cls, values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        return _validate_searching_result(values)


class ProfilesScoringData(BaseModel):
    predictions: t.List[conlist(confloat(ge=0, le=1), min_length=2, max_length=2)]
    profiles: t.List[Profile]


class ProfilesScoringResponse(HrFlowAPIResponseWithPagination):
    data: ProfilesScoringData

    @model_validator(mode="before")
    @classmethod
    def _check(cls, values: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
        return _validate_scoring_result(values)


class ProfileAskingResponse(HrFlowAPIResponse):
    data: t.Optional[t.List[str]] = None


class ProfileUnfoldingData(BaseModel):
    experiences: t.List[Experience]


class ProfileUnfoldingResponse(HrFlowAPIResponse):
    data: t.Optional[ProfileUnfoldingData] = None


class ProfileArchieveData(BaseModel):
    key: constr(pattern=KEY_REGEX)


class ProfileArchiveResponse(HrFlowAPIResponse):
    data: t.Optional[ProfileArchieveData] = None

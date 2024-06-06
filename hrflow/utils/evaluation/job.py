import typing as t

from openpyxl.utils.cell import get_column_interval
from openpyxl.worksheet.worksheet import Worksheet
from pydantic import BaseModel
from tqdm import tqdm

TEMPLATE_URL = "https://riminder-documents-eu-2019-12-dev.s3.eu-west-1.amazonaws.com/evaluation/parsing-evaluation-template-v3-job.xlsx"  # noqa: E501
START_ROW_ID = 5

NAME_COLUMN_ID = "A"
URL_COLUMN_ID = "B"
KEY_COLUMN_ID = "C"

OVERVIEW_FIELD_LIST = (
    "score",
    "name",
    "location",
    "summary",
    "culture",
    "benefits",
    "responsibilities",
    "requirements",
    "interviews",
)
INFO_START_COLUMN_ID, INFO_END_COLUMN_ID = ("D", "L")

RANGES_FLOATS_FIELD_LIST = (
    "score",
    "count",
    "name",
    "value_min",
    "value_max",
    "unit",
)
EXPERIENCE_START_COLUMN_ID, EXPERIENCE_END_COLUMN_ID = ("M", "R")

RANGES_DATES_FIELD_LIST = (
    "score",
    "count",
    "name",
    "value_min",
    "value_max",
)
EDUCATION_START_COLUMN_ID, EDUCATION_END_COLUMN_ID = ("S", "W")

OTHER_FIELD_LIST = (
    "skills",
    "languages",
    "tasks",
    "courses",
    "certifications",
)
OTHER_START_COLUMN_ID, OTHER_END_COLUMN_ID = ("X", "AB")


class OverviewEvaluation(BaseModel):
    score: float
    name: int
    location: int
    summary: int
    culture: int
    benefits: int
    responsibilities: int
    requirements: int
    interviews: int

    @staticmethod
    def from_job(job: t.Dict[str, t.Any]) -> "OverviewEvaluation":
        name = 1 if job.get("name") else 0
        location = 1 if job.get("location", {}).get("text") else 0
        summary = 1 if job.get("summary") else 0
        culture = 1 if job.get("culture") else 0
        benefits = 1 if job.get("benefits") else 0
        responsibilities = 1 if job.get("responsibilities") else 0
        requirements = 1 if job.get("requirements") else 0
        interviews = 1 if job.get("interviews") else 0

        score = (
            name
            + location
            + summary
            + culture
            + benefits
            + responsibilities
            + requirements
            + interviews
        )
        score /= 8
        return OverviewEvaluation(
            score=score,
            name=name,
            location=location,
            summary=summary,
            culture=culture,
            benefits=benefits,
            responsibilities=responsibilities,
            requirements=requirements,
            interviews=interviews,
        )


class RangeFloatEvaluation(BaseModel):
    score: float
    count: int
    name: float
    value_min: float
    value_max: float
    unit: float

    @staticmethod
    def from_job(job: t.Dict[str, t.Any]) -> "RangeFloatEvaluation":
        count = len(job.get("ranges_float", []))

        name = 0
        value_min = 0
        value_max = 0
        unit = 0
        for range_float in job.get("ranges_floats", []):
            name += 1 if range_float.get("name") else 0
            value_min += 1 if range_float.get("value_min") else 0
            value_max += 1 if range_float.get("value_max") else 0
            unit += 1 if range_float.get("unit") else 0

        if count > 0:
            name /= count
            value_min /= count
            value_max /= count
            unit /= count

        score = name + value_min + value_max + unit
        score /= 4

        return RangeFloatEvaluation(
            score=score,
            count=count,
            name=name,
            value_min=value_min,
            value_max=value_max,
            unit=unit,
        )


class RangeDateEvaluation(BaseModel):
    score: float
    count: int
    name: float
    value_min: float
    value_max: float

    @staticmethod
    def from_job(job: t.Dict[str, t.Any]) -> "RangeDateEvaluation":
        count = len(job.get("ranges_date", []))

        name = 0
        value_min = 0
        value_max = 0
        for range_date in job.get("ranges_dates", []):
            name += 1 if range_date.get("name") else 0
            value_min += 1 if range_date.get("value_min") else 0
            value_max += 1 if range_date.get("value_max") else 0

        if count > 0:
            name /= count
            value_min /= count
            value_max /= count

        score = name + value_min + value_max
        score /= 3

        return RangeDateEvaluation(
            score=score,
            count=count,
            name=name,
            value_min=value_min,
            value_max=value_max,
        )


class OtherEvaluation(BaseModel):
    skills: int
    languages: int
    tasks: int
    courses: int
    certifications: int

    @staticmethod
    def from_job(job: t.Dict[str, t.Any]) -> "OtherEvaluation":
        skills = len(job.get("skills", []))
        languages = len(job.get("languages", []))
        tasks = len(job.get("tasks", []))
        courses = len(job.get("courses", []))
        certifications = len(job.get("certifications", []))

        return OtherEvaluation(
            skills=skills,
            languages=languages,
            tasks=tasks,
            courses=courses,
            certifications=certifications,
        )


class JobEvaluation(BaseModel):
    overview: OverviewEvaluation
    range_float: RangeFloatEvaluation
    range_date: RangeDateEvaluation
    other: OtherEvaluation

    name: str
    url: str
    key: str

    @staticmethod
    def from_job(job: t.Dict[str, t.Any]) -> "JobEvaluation":
        return JobEvaluation(
            overview=OverviewEvaluation.from_job(job),
            range_float=RangeFloatEvaluation.from_job(job),
            range_date=RangeDateEvaluation.from_job(job),
            other=OtherEvaluation.from_job(job),
            name=job.get("name") or "",
            url=job.get("url") or "",
            key=job.get("key") or "",
        )


def parsing_evaluator(
    job_list: t.List[t.Dict[str, t.Any]], show_progress: bool = False
) -> t.List[JobEvaluation]:
    """
    Evaluate a list of jobs

    Args:
        job_list:           <List[Dict[str, Any]>>
                                 List of jobs
        show_progress:          <bool>
                                 Show the progress bar

    Returns:
        <List[JobEvaluation]>:
        List of job evaluations
    """
    if show_progress:
        job_list = tqdm(job_list, desc="Evaluating jobs")
    return [JobEvaluation.from_job(job) for job in job_list]


def fill_metadata(
    work_sheet: Worksheet,
    job_eval_list: t.List[JobEvaluation],
    show_progress: bool = False,
) -> None:
    """
    Fill the metadata of the jobs in the worksheet

    Args:
        work_sheet:                  <Worksheet>
                                     The worksheet to fill
        job_eval_list:           <List[JobEvaluation]>
                                     The list of job evaluations
        show_progress:               <bool>
                                     Show the progress bar
    """
    if show_progress:
        job_eval_list = tqdm(job_eval_list, desc="Filling meta-data")
    for row_id, job_eval in enumerate(job_eval_list, START_ROW_ID):
        work_sheet[f"{NAME_COLUMN_ID}{row_id}"].value = job_eval.name
        work_sheet[f"{KEY_COLUMN_ID}{row_id}"].value = job_eval.key
        if job_eval.url:
            work_sheet[f"{URL_COLUMN_ID}{row_id}"].hyperlink = job_eval.url


def fill_overview(
    work_sheet: Worksheet,
    job_eval_list: t.List[JobEvaluation],
    show_progress: bool = False,
) -> None:
    """
    Fill the overview scores of the jobs in the worksheet

    Args:
        work_sheet:                  <Worksheet>
                                     The worksheet to fill
        job_eval_list:           <List[JobEvaluation]>
                                     The list of job evaluations
        show_progress:               <bool>
                                     Show the progress bar
    """
    colum_id_list = get_column_interval(INFO_START_COLUMN_ID, INFO_END_COLUMN_ID)
    if show_progress:
        job_eval_list = tqdm(job_eval_list, desc="Filling overview scores")
    for row_id, job_eval in enumerate(job_eval_list, START_ROW_ID):
        for column_id, field in zip(colum_id_list, OVERVIEW_FIELD_LIST):
            work_sheet[f"{column_id}{row_id}"].value = getattr(job_eval.overview, field)


def fill_range_float(
    work_sheet: Worksheet,
    job_eval_list: t.List[JobEvaluation],
    show_progress: bool = False,
) -> None:
    """
    Fill the range float scores of the jobs in the worksheet

    Args:
        work_sheet:                  <Worksheet>
                                     The worksheet to fill
        job_eval_list:           <List[JobEvaluation]>
                                     The list of job evaluations
        show_progress:               <bool>
                                     Show the progress bar
    """
    colum_id_list = get_column_interval(
        EXPERIENCE_START_COLUMN_ID, EXPERIENCE_END_COLUMN_ID
    )
    if show_progress:
        job_eval_list = tqdm(job_eval_list, desc="Filling range float scores")
    for row_id, job_eval in enumerate(job_eval_list, START_ROW_ID):
        for column_id, field in zip(colum_id_list, RANGES_FLOATS_FIELD_LIST):
            work_sheet[f"{column_id}{row_id}"].value = getattr(
                job_eval.range_float, field
            )


def fill_range_date(
    work_sheet: Worksheet,
    job_eval_list: t.List[JobEvaluation],
    show_progress: bool = False,
) -> None:
    """
    Fill the range date scores of the jobs in the worksheet

    Args:
        work_sheet:                  <Worksheet>
                                     The worksheet to fill
        job_eval_list:           <List[JobEvaluation]>
                                     The list of job evaluations
        show_progress:               <bool>
                                     Show the progress bar
    """
    colum_id_list = get_column_interval(
        EDUCATION_START_COLUMN_ID, EDUCATION_END_COLUMN_ID
    )
    if show_progress:
        job_eval_list = tqdm(job_eval_list, desc="Filling range date scores")
    for row_id, job_eval in enumerate(job_eval_list, START_ROW_ID):
        for column_id, field in zip(colum_id_list, RANGES_DATES_FIELD_LIST):
            work_sheet[f"{column_id}{row_id}"].value = getattr(
                job_eval.range_date, field
            )


def fill_other(
    work_sheet: Worksheet,
    job_eval_list: t.List[JobEvaluation],
    show_progress: bool = False,
) -> None:
    """
    Fill the other scores of the jobs in the worksheet

    Args:
        work_sheet:                  <Worksheet>
                                     The worksheet to fill
        job_eval_list:           <List[JobEvaluation]>
                                     The list of job evaluations
        show_progress:               <bool>
                                     Show the progress bar
    """
    colum_id_list = get_column_interval(OTHER_START_COLUMN_ID, OTHER_END_COLUMN_ID)
    if show_progress:
        job_eval_list = tqdm(job_eval_list, desc="Filling other scores")
    for row_id, job_eval in enumerate(job_eval_list, START_ROW_ID):
        for column_id, field in zip(colum_id_list, OTHER_FIELD_LIST):
            work_sheet[f"{column_id}{row_id}"].value = getattr(job_eval.other, field)


def fill_work_sheet(
    work_sheet: Worksheet,
    job_eval_list: t.List[JobEvaluation],
    show_progress: bool = False,
) -> None:
    """
    Fill the work sheet with the job evaluations

    Args:
        work_sheet:                  <Worksheet>
                                     The worksheet to fill
        job_eval_list:           <List[JobEvaluation]>
                                     The list of job evaluations
        show_progress:               <bool>
                                     Show the progress bar
    """
    fill_metadata(work_sheet, job_eval_list, show_progress)
    fill_overview(work_sheet, job_eval_list, show_progress)
    fill_range_float(work_sheet, job_eval_list, show_progress)
    fill_range_date(work_sheet, job_eval_list, show_progress)
    fill_other(work_sheet, job_eval_list, show_progress)

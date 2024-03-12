import typing as t
from uuid import uuid1

import pytest
from requests import codes as http_codes

from hrflow import Hrflow

from .utils.schemas import (
    JobArchiveResponse,
    JobAskingResponse,
    JobIndexingResponse,
    JobsScoringResponse,
    JobsSearchingResponse,
)
from .utils.tools import (
    _check_same_keys_equality,
    _indexed_response_get,
    _now_iso8601_get,
    _var_from_env_get,
)


@pytest.fixture(scope="module")
def hrflow_client():
    return Hrflow(
        api_secret=_var_from_env_get("HRFLOW_API_KEY"),
        api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
    )


def _job_get() -> t.Dict[str, t.Any]:
    return dict(
        reference=str(uuid1()),
        name="r&d engineer",
        location=dict(text="7 rue 4 septembre paris", lat=48.869179, lng=2.33814),
        sections=[
            dict(
                name="Description",
                title="Description",
                description=(
                    "As an AI Researcher Intern at HrFlow.ai, you'll play a vital role"
                    " in driving the next phase of our exciting expansion. Your role"
                    " involves developing innovative AI models and algorithms to tackle"
                    " intricate HR challenges. Collaborating with fellow researchers"
                    " and engineers, you'll help guide the technical direction and"
                    " architecture of our AI solutions."
                ),
            )
        ],
        url="https://www.linkedin.com/jobs/search/?currentJobId=3718625295",
        summary=(
            "As an AI Researcher Intern at HrFlow.ai, you'll play a vital role in"
            " driving the next phase of our exciting expansion. Your role involves"
            " developing innovative AI models and algorithms to tackle intricate HR"
            " challenges. Collaborating with fellow researchers and engineers, you'll"
            " help guide the technical direction and architecture of our AI solutions."
        ),
        created_at=_now_iso8601_get(),
        skills=[dict(name="Deep Learning", type="hard", value="95/100")],
        languages=[dict(name="French", value="Fluent")],
        certifications=[dict(name="ISO 27001", value="Individual")],
        courses=[dict(name="Statistical Learning", value="On campus")],
        tasks=[dict(name="Developing innovative AI models", value="Innovating")],
        tags=[dict(name="Curios", value="1")],
        metadatas=[
            dict(name="Interview note", value="Today, I met an amazing candidate...")
        ],
        ranges_float=[
            dict(name="salary", value_min=1234.56, value_max=6543.21, unit="euros")
        ],
        ranges_date=[
            dict(
                name="dates",
                value_min="2023-06-01T23:00:00.000Z",
                value_max="2023-09-01T23:00:00.000Z",
            )
        ],
        culture="We love AI engineering, problem-solving, and business.",
        responsibilities=(
            "Designing, implementing, and optimizing AI models and algorithms that"
            " solve complex HR challenges. Analyzing and evaluating the performance of"
            " AI models and algorithms. Collaborating with other researchers and"
            " engineers to improve the overall performance and accuracy of our AI"
            " solutions. Staying up-to-date with the latest developments in AI research"
            " and technology. Communicating and presenting research findings to"
            " internal and external stakeholders."
        ),
        requirements=(
            "Enrolled in an advanced degree in Computer Science, Artificial"
            " Intelligence, or a related field. Proficiency in developing and"
            " implementing AI models and algorithms. Strong programming skills in"
            " Python. Experience with deep learning frameworks like TensorFlow,"
            " PyTorch, or Keras. Solid grasp of machine learning fundamentals and"
            " statistical analysis. Exceptional problem-solving and analytical"
            " abilities. Effective communication and collaboration skills."
        ),
        interviews=(
            "Interview with one of our lead AI Researcher to discuss your experience"
            " and qualifications in more detail. Interview with our Chief Executive"
            " Officer to discuss your fit within our organization and your career"
            " goals."
        ),
        benefits=(
            "Go fast and learn a lot. High-impact position and responsibilities without"
            " any day being the same. Competitive salary and variable compensation. Gym"
            " club & public transportation. Fun & smart colleagues. Latest hardware."
        ),
    )


@pytest.mark.job
@pytest.mark.indexing
def test_job_indexing_basic(hrflow_client):
    job = _job_get()
    model = JobIndexingResponse.parse_obj(
        hrflow_client.job.storing.add_json(
            board_key=_var_from_env_get("HRFLOW_BOARD_KEY"),
            job_json=job,
        )
    )
    assert model.code == http_codes.created
    assert model.data is not None
    _check_same_keys_equality(job, model.data)


@pytest.mark.job
@pytest.mark.searching
def test_job_searching_basic(hrflow_client):
    model = JobsSearchingResponse.parse_obj(
        hrflow_client.job.searching.list(
            board_keys=[_var_from_env_get("HRFLOW_BOARD_KEY")],
            limit=5,  # allows to bypass the bug with archived jobs
        )
    )
    assert model.code == http_codes.ok
    assert len(model.data.jobs) == model.meta.count


@pytest.mark.job
@pytest.mark.scoring
def test_job_scoring_basic(hrflow_client):
    model = JobsScoringResponse.parse_obj(
        hrflow_client.job.scoring.list(
            algorithm_key=_var_from_env_get("HRFLOW_ALGORITHM_KEY"),
            board_keys=[_var_from_env_get("HRFLOW_BOARD_KEY")],
            profile_key=_var_from_env_get("HRFLOW_PROFILE_KEY"),
            source_key=_var_from_env_get("HRFLOW_SOURCE_KEY_QUICKSILVER_SYNC"),
            limit=5,  # allows to bypass the bug with archived jobs
        )
    )
    assert (
        model.code == http_codes.ok
    ), "Maybe the job is not already indexed for the scoring. Please, try again later."
    assert len(model.data.jobs) == len(model.data.predictions)


@pytest.mark.job
@pytest.mark.asking
def test_job_asking_basic(hrflow_client):
    BOARD_KEY = _var_from_env_get("HRFLOW_BOARD_KEY")
    model = JobAskingResponse.parse_obj(
        hrflow_client.job.asking.get(
            board_key=BOARD_KEY,
            key=_indexed_response_get(hrflow_client, BOARD_KEY, _job_get()).data.key,
            questions=[
                "What is the company proposing this job offer ?",
            ],
        )
    )
    assert model.code == http_codes.ok
    assert len(model.data) == 1
    assert "hrflow.ai" in model.data[0].lower()


@pytest.mark.skip(reason="backend: multiple questions are not correctly handled yet")
@pytest.mark.job
@pytest.mark.asking
def test_job_asking_multiple_questions(hrflow_client):
    BOARD_KEY = _var_from_env_get("HRFLOW_BOARD_KEY")
    questions = [
        "What is the job title ?",
        "What is the company proposing this job offer ?",
        "What is the job location address ?",
        "What are the expected skills for this job ?",
    ]
    model = JobAskingResponse.parse_obj(
        hrflow_client.job.asking.get(
            board_key=BOARD_KEY,
            key=_indexed_response_get(hrflow_client, BOARD_KEY, _job_get()).data.key,
            questions=questions,
        )
    )
    assert model.code == http_codes.ok
    assert len(model.data) == len(questions)
    assert "r&d engineer" in model.data[0].lower()
    assert "hrflow.ai" in model.data[1].lower()
    assert "7 rue 4 septembre" in model.data[2].lower()
    assert "deep learning" in model.data[3].lower()


@pytest.mark.job
@pytest.mark.asking
def test_job_asking_no_questions(hrflow_client):
    BOARD_KEY = _var_from_env_get("HRFLOW_BOARD_KEY")
    model = JobAskingResponse.parse_obj(
        hrflow_client.job.asking.get(
            board_key=BOARD_KEY,
            key=_indexed_response_get(hrflow_client, BOARD_KEY, _job_get()).data.key,
            questions=None,
        )
    )
    assert model.code == http_codes.bad_request


@pytest.mark.job
@pytest.mark.archive
def test_job_archive_basic(hrflow_client):
    BOARD_KEY = _var_from_env_get("HRFLOW_BOARD_KEY")
    mock_key = _indexed_response_get(hrflow_client, BOARD_KEY, _job_get()).data.key
    model = JobArchiveResponse.parse_obj(
        hrflow_client.job.storing.archive(board_key=BOARD_KEY, key=mock_key)
    )
    assert model.code == http_codes.ok
    assert model.data.key == mock_key


@pytest.mark.job
@pytest.mark.editing
def test_job_editing_basic(hrflow_client):
    BOARD_KEY = _var_from_env_get("HRFLOW_BOARD_KEY")
    mock_job = _indexed_response_get(hrflow_client, BOARD_KEY, _job_get()).data
    mock_job.interviews = (
        f"To access the interview call you must use the token {uuid1()}."
    )
    model = JobIndexingResponse.parse_obj(
        hrflow_client.job.storing.edit(
            board_key=BOARD_KEY,
            job_json=mock_job.dict(),
        )
    )
    assert model.code == http_codes.ok
    assert model.data.interviews == mock_job.interviews

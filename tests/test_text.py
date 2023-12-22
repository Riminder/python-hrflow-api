import typing as t

import pytest
import requests

from hrflow import Hrflow

from .utils.enums import TAGGING_ALGORITHM
from .utils.schemas import (
    TextEmbeddingResponse,
    TextImagingResponse,
    TextLinkingResponse,
    TextOCRResponse,
    TextParsingResponse,
    TextTaggingDataItem,
    TextTaggingReponse,
)
from .utils.tools import _file_get, _var_from_env_get

TAGGING_TEXTS = [
    (
        "Data Insights Corp. is seeking a Senior Data Scientist for a"
        " contract-to-direct position. You will be responsible for designing and"
        " implementing advanced machine learning algorithms and playing a key role in"
        " shaping our data science initiatives. The CDI arrangement offers a pathway to"
        " a full-time role"
    ),
    (
        "DataTech Solutions is hiring a Data Scientist for a fixed-term contract of 12"
        " months. You will work on various data analysis and modeling projects and"
        " assisting in short-term projects; with the possibility of extension or"
        " permanent roles"
    ),
]


@pytest.fixture(scope="module")
def hrflow_client():
    return Hrflow(
        api_secret=_var_from_env_get("HRFLOW_API_KEY"),
        api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
    )


@pytest.mark.text
@pytest.mark.embedding
def test_embedding_basic(hrflow_client):
    text = "I love using embeddings in order do transfer learning with my AI algorithms"
    model = TextEmbeddingResponse.model_validate(
        hrflow_client.text.embedding.post(text=text)
    )
    assert model.code == requests.codes.ok
    assert len(model.data) > 0


@pytest.mark.text
@pytest.mark.embedding
def test_embedding_no_text(hrflow_client):
    model = TextEmbeddingResponse.model_validate(
        hrflow_client.text.embedding.post(text=None)
    )
    assert model.code == requests.codes.bad_request
    assert "null" in model.message.lower()


def _image_sizes_get(content: bytes) -> int:
    w = int.from_bytes(content[16:20], byteorder="big")
    h = int.from_bytes(content[20:24], byteorder="big")
    return w, h


def _content_is_png(content: bytes) -> bool:
    return content.startswith(b"\x89PNG\r\n\x1a\n")


def _imaging_test_valid_size(width: t.Literal[256, 512]):
    model = TextImagingResponse.model_validate(
        Hrflow(
            api_secret=_var_from_env_get("HRFLOW_API_KEY"),
            api_user=_var_from_env_get("HRFLOW_USER_EMAIL"),
        ).text.imaging.post(text="plumber", width=width)
    )
    assert model.code == requests.codes.ok
    response = requests.get(model.data.image_url)
    assert response.status_code == requests.codes.ok
    assert _content_is_png(response.content)
    assert _image_sizes_get(response.content) == (width, width)


@pytest.mark.text
@pytest.mark.imaging
def test_imaging_basic_256():
    _imaging_test_valid_size(256)


@pytest.mark.text
@pytest.mark.imaging
def test_imaging_basic_512():
    _imaging_test_valid_size(512)


@pytest.mark.text
@pytest.mark.imaging
def test_imaging_unsupported_size(hrflow_client):
    model = TextImagingResponse.model_validate(
        hrflow_client.text.imaging.post(text="mechanic", width=111)
    )
    assert model.code == requests.codes.bad_request
    assert "111" in model.message


@pytest.mark.text
@pytest.mark.imaging
def test_imaging_no_text(hrflow_client):
    model = TextImagingResponse.model_validate(
        hrflow_client.text.imaging.post(text=None, width=256)
    )
    assert model.code == requests.codes.bad_request
    assert "null" in model.message.lower()


@pytest.mark.text
@pytest.mark.linking
def test_linking_basic(hrflow_client):
    top_n = 7
    model = TextLinkingResponse.model_validate(
        hrflow_client.text.linking.post(word="ai", top_n=top_n)
    )
    assert model.code == requests.codes.ok
    assert len(model.data) == top_n


@pytest.mark.text
@pytest.mark.linking
def test_linking_no_text(hrflow_client):
    model = TextLinkingResponse.model_validate(
        hrflow_client.text.linking.post(word=None, top_n=1)
    )
    assert model.code == requests.codes.bad_request
    assert "null" in model.message.lower()


@pytest.mark.text
@pytest.mark.linking
def test_linking_zero(hrflow_client):
    model = TextLinkingResponse.model_validate(
        hrflow_client.text.linking.post(word="ai", top_n=0)
    )
    assert model.code == requests.codes.ok
    assert len(model.data) == 0


@pytest.mark.text
@pytest.mark.linking
@pytest.mark.skip(reason="backend: negative top_n not correctly handled yet")
def test_linking_negative_amount(hrflow_client):
    model = TextLinkingResponse.model_validate(
        hrflow_client.text.linking.post(word="ai", top_n=-42)
    )
    assert model.code == requests.codes.bad_request


@pytest.mark.text
@pytest.mark.tagging
def test_tagger_rome_family_with_text_param(hrflow_client):
    model = TextTaggingReponse.model_validate(
        hrflow_client.text.tagging.post(
            algorithm_key=TAGGING_ALGORITHM.TAGGER_ROME_FAMILY,
            text=TAGGING_TEXTS[0],
            top_n=2,
        )
    )
    assert model.code == requests.codes.ok
    assert isinstance(model.data, TextTaggingDataItem)


@pytest.mark.text
@pytest.mark.tagging
def test_tagger_rome_family_with_texts_param(hrflow_client):
    model = TextTaggingReponse.model_validate(
        hrflow_client.text.tagging.post(
            algorithm_key=TAGGING_ALGORITHM.TAGGER_ROME_FAMILY,
            texts=TAGGING_TEXTS,
            top_n=2,
        )
    )
    assert model.code == requests.codes.ok
    assert isinstance(model.data, list)
    assert len(model.data) == len(TAGGING_TEXTS)


@pytest.mark.text
@pytest.mark.tagging
def test_tagger_rome_family_with_text_and_texts_param(hrflow_client):
    try:
        TextTaggingReponse.model_validate(
            hrflow_client.text.tagging.post(
                algorithm_key=TAGGING_ALGORITHM.TAGGER_ROME_FAMILY,
                text=TAGGING_TEXTS[0],
                texts=TAGGING_TEXTS,
                top_n=2,
            )
        )
        pytest.fail("Should have raised a ValueError")
    except ValueError:
        pass


@pytest.mark.text
@pytest.mark.tagging
def test_tagger_rome_family_without_text_or_texts_param(hrflow_client):
    try:
        TextTaggingReponse.model_validate(
            hrflow_client.text.tagging.post(
                algorithm_key=TAGGING_ALGORITHM.TAGGER_ROME_FAMILY,
                top_n=2,
            )
        )
        pytest.fail("Should have raised a ValueError")
    except ValueError:
        pass


def _tagging_test(
    hrflow_client: Hrflow,
    algorithm_key: TAGGING_ALGORITHM,
    texts: t.List[str],
    context: t.Optional[str] = None,
    labels: t.Optional[t.List[str]] = None,
    top_n: t.Optional[int] = 1,
) -> TextTaggingReponse:
    model = TextTaggingReponse.model_validate(
        hrflow_client.text.tagging.post(
            algorithm_key=algorithm_key,
            texts=texts,
            context=context,
            labels=labels,
            top_n=top_n,
        )
    )
    assert model.code == requests.codes.ok
    assert len(model.data) == len(texts)
    if algorithm_key == TAGGING_ALGORITHM.TAGGER_HRFLOW_LABELS:
        assert all(
            all(
                tag in labels or pytest.fail(f"{tag} not in {labels}")
                for tag in item.tags
            )
            and (
                all(
                    id.isnumeric() or pytest.fail(f"{id} is not numerical")
                    for id in item.ids
                )
            )
            for item in model.data
        )
    return model


@pytest.mark.text
@pytest.mark.tagging
def test_tagger_rome_family_basic(hrflow_client):
    _tagging_test(
        hrflow_client=hrflow_client,
        algorithm_key=TAGGING_ALGORITHM.TAGGER_ROME_FAMILY,
        texts=TAGGING_TEXTS,
        top_n=2,
    )


@pytest.mark.text
@pytest.mark.tagging
def test_tagger_rome_subfamily_basic(hrflow_client):
    _tagging_test(
        hrflow_client=hrflow_client,
        algorithm_key=TAGGING_ALGORITHM.TAGGER_ROME_SUBFAMILY,
        texts=TAGGING_TEXTS,
        top_n=3,
    )


@pytest.mark.text
@pytest.mark.tagging
def test_tagger_rome_category_basic(hrflow_client):
    _tagging_test(
        hrflow_client=hrflow_client,
        algorithm_key=TAGGING_ALGORITHM.TAGGER_ROME_CATEGORY,
        texts=TAGGING_TEXTS,
        top_n=4,
    )


@pytest.mark.text
@pytest.mark.tagging
def test_tagger_rome_jobtitle_basic(hrflow_client):
    _tagging_test(
        hrflow_client=hrflow_client,
        algorithm_key=TAGGING_ALGORITHM.TAGGER_ROME_JOBTITLE,
        texts=TAGGING_TEXTS,
        top_n=5,
    )


@pytest.mark.text
@pytest.mark.tagging
def test_tagger_hrflow_skills_basic(hrflow_client):
    _tagging_test(
        hrflow_client=hrflow_client,
        algorithm_key=TAGGING_ALGORITHM.TAGGER_HRFLOW_SKILLS,
        texts=TAGGING_TEXTS,
        top_n=6,
    )


@pytest.mark.text
@pytest.mark.tagging
def test_tagger_hrflow_labels_basic(hrflow_client):
    model = _tagging_test(
        hrflow_client=hrflow_client,
        algorithm_key=TAGGING_ALGORITHM.TAGGER_HRFLOW_LABELS,
        texts=TAGGING_TEXTS,
        context=(
            "The CDI is a Contrat à Durée Indeterminée - essentially an open-ended or"
            " permanent employment contract. The CDD is a Contrat à Durée Determinée -"
            " a fixed-term or temporary employment contract. These are the two most"
            " common types but by no means the only form of French employment contract."
            " The contracts have to be drawn up by the employer, who must ensure that"
            " it's legally the correct type for the circumstances."
        ),
        labels=["CDI", "CDD"],
    )
    assert model.data[0].tags[0] == "CDI"
    assert model.data[1].tags[0] == "CDD"


@pytest.mark.text
@pytest.mark.tagging
def test_tagger_hrflow_labels_no_context(hrflow_client):
    model = _tagging_test(
        hrflow_client=hrflow_client,
        algorithm_key=TAGGING_ALGORITHM.TAGGER_HRFLOW_LABELS,
        texts=[
            (
                "In the quantum gardens of knowledge, she cultivates algorithms,"
                " weaving threads of brilliance through the binary blooms, a sorceress"
                " of AI enchantment."
            ),
            (
                "In the neural realms of innovation, he navigates the data currents,"
                " sculpting insights from the digital ether, a virtuoso of AI"
                " exploration."
            ),
        ],
        labels=["male", "female"],
    )
    assert model.data[0].tags[0] == "female"
    assert model.data[1].tags[0] == "male"


@pytest.mark.text
@pytest.mark.ocr
def test_ocr_basic(hrflow_client):
    s3_url = """https://riminder-documents-eu-2019-12.s3-eu-west-1.amazonaws.com/\
teams/fc9d40fd60e679119130ea74ae1d34a3e22174f2/sources/07065e555609a231752a586afd6\
495c951bbae6b/profiles/52e3c23a5f21190c59f53c41b5630ecb5d414f94/parsing/resume.pdf"""
    file = _file_get(s3_url, "ocr")
    assert file is not None
    model = TextOCRResponse.model_validate(hrflow_client.text.ocr.post(file=file))
    assert model.code == requests.codes.ok
    assert "ocr" in model.message.lower()


@pytest.mark.text
@pytest.mark.parsing
def test_parsing_basic(hrflow_client):
    texts = ["John Doe can be contacted on john.doe@hrflow.ai"]
    model = TextParsingResponse.model_validate(
        hrflow_client.text.parsing.post(texts=texts)
    )
    assert model.code == requests.codes.ok
    assert len(model.data) == len(texts)

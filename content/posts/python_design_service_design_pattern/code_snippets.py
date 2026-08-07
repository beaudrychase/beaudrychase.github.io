from abc import ABC, abstractmethod
import os
from unittest.mock import Mock, call

from pytest import fixture
from pytest_mock import MockerFixture


class Rejection:
    reason: str
    confidence: float


class RejectionFetcher(ABC):

    @abstractmethod
    def get_rejection(
        self,
        question: str,
    ) -> Rejection:
        pass


class QuestionAnswerer:
    _rejection_fetcher: RejectionFetcher
    _default_answer: str

    def __init__(
        self,
        rejection_fetcher: RejectionFetcher,
        default_answer: str,
    ):
        self._rejection_fetcher = (
            rejection_fetcher
        )
        self._default_answer = (
            default_answer
        )

    def get_response(
        self, question: str
    ) -> str:
        rejection = self._rejection_fetcher.get_rejection(
            question
        )
        if rejection.confidence < 0.5:
            return self._default_answer

        return rejection.reason


# Application code
requests: list[str]
rejection_fetcher: RejectionFetcher

question_answerer = QuestionAnswerer(
    rejection_fetcher,
    os.environ["DEFAULT_RESPONSE"],
)
answers: list[str] = list()
for request in requests:
    answers.append(
        question_answerer.get_response(
            request
        )
    )

# integration test

DEFAULT_RESPONSE = "default response"


@fixture
def rejection_fetcher() -> RejectionFetcher:
    pass


@fixture
def question_answerer(
    rejection_fetcher: RejectionFetcher,
) -> QuestionAnswerer:
    return QuestionAnswerer(
        rejection_fetcher, DEFAULT_RESPONSE
    )


def test_get_response_simple_question_doesnt_use_default(
    question_answerer: QuestionAnswerer,
):
    example_question = (
        "Could you help me with this?"
    )

    result = question_answerer.get_response(
        example_question
    )

    assert result != DEFAULT_RESPONSE


def test_get_response_vague_question_uses_default(
    question_answerer: QuestionAnswerer,
):
    vague_question = "???"

    result = question_answerer.get_response(
        vague_question
    )

    assert result == DEFAULT_RESPONSE


# unit test

FETCHED_REJECTION = "fetched rejection"
DEFAULT_REJECTION = "default rejection"
EXAMPLE_QUESTION = "example question"


@fixture
def rejection(
    mocker: MockerFixture,
) -> Rejection:
    rejection = mocker.Mock(
        spec=Rejection,
        reason=FETCHED_REJECTION,
        confidence=0.90,
    )
    return rejection


@fixture
def rejection_fetcher(
    mocker: MockerFixture, rejection: Mock
) -> Mock:
    rejection_fetcher = mocker.Mock(
        spec=RejectionFetcher
    )
    rejection_fetcher.get_rejection.return_value = (
        rejection
    )
    return rejection_fetcher


@fixture
def question_answerer(
    rejection_fetcher: Mock,
) -> QuestionAnswerer:
    return QuestionAnswerer(
        rejection_fetcher, DEFAULT_REJECTION
    )


def test_get_response_high_confidence_fetched_result_returns_fetched(
    question_answerer: QuestionAnswerer,
    rejection_fetcher: Mock,
):

    result = question_answerer.get_response(
        EXAMPLE_QUESTION
    )

    assert result == FETCHED_REJECTION
    assert (
        rejection_fetcher.get_rejection.call_args
        == call(EXAMPLE_QUESTION)
    )


def test_get_response_low_confidence_fetched_result_returns_default(
    question_answerer: QuestionAnswerer,
    rejection_fetcher: Mock,
    rejection: Mock,
):
    rejection.confidence = 0.00

    result = question_answerer.get_response(
        EXAMPLE_QUESTION
    )

    assert result == DEFAULT_REJECTION
    assert (
        rejection_fetcher.get_rejection.call_args
        == call(EXAMPLE_QUESTION)
    )

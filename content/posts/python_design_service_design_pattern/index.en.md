---
title: "Python Service Design Patterns"
date: 2026-08-06T15:15:38-05:00
summary: "Introducing high level OOP class design for services in python"
slug: "python-service-design-patterns"
Tags: []
Categories: ["design"]
DisableComments: false
Draft: true
featured_image: "living_light_front.jpeg"
---

In this post I want to share a very common design pattern I use when making
classes in python. I will go over the high level design, a simple example, and how to write integration and unit tests against the pattern. My goal is to

## What is living_light

```python {linenos=inline}

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

```

living_light is a decorative lamp that slowly rises and falls in brightness at
the rate of meditative breathing. The color and brightness follow the day's
natural progression and our circadian rhythms. During the day, it is a bright
blueish-white and then at sunset, it transitions to a dark red for the night.
This lighting cycle follows research on the impact exposure to different colored
light has on our ability to sleep at night. Exposure to blue and white light
during the day helps you fall asleep at night, while exposure to them at night
can make it hard to sleep ([source](https://pubmed.ncbi.nlm.nih.gov/25535358/)).
Red light, on the other hand, has little effect on our circadian rhythms, so
exposure at night minimally impacts sleep
([source](https://pubmed.ncbi.nlm.nih.gov/30311830/)). The light serves as an
open invitation to pause to take a breath and a reminder to tap into nature and
follow our biological rythm and the Earth's solar cycle.

{{% figure src="living_light_back.jpeg" %}} Back of LED grid {{% /figure %}}

Currently the light intentionally has a very limited user interface. I had spent
a lot of time implementing a text interface to change the behavior of the light
through Telegram messenger's bot API that would take simple commands to change
the length of the breath cycle, the color, and brightness. However, I found that
having these options changed the way I engaged with the light; I found myself
distracted by assessing whether or not I should change the settings instead of
meditating with it. Having these options detracted from the experience I
designed, so I removed them. The interface is now intentionally restrained, the
only way to interact with it is to look at it.

## My Development Journey

I began working on this project Summer of 2020. I had just finished the first
semester of online classes after the pandemic upended in person activities. I
had my first internship that summer, while the world was still transitioning to
work from home. Suddenly my world was circumscribed to my childhood bedroom and
my internet connection. Between navigating online work, social isolation, and
doomscrolling, my mental health declined.

This project is my reaction against that time of my life. At a time when
everything I did was online, I wanted to work on something I could hold, see,
and feel. When I felt distracted, anxious, and not present I wanted to build
something to help me feel grounded in the present. I wanted a reminder that even
though everything else was interrupted, the cycle of the day continues. Thus the
project began to take shape.

{{% figure src="living_light_early_prototype.jpeg" %}} Early prototype running
on an Arduino Uno.{{% /figure %}}

I've been incrementally and intermittantly working on the project ever since. It
has been a fun project to work with and I'm happy that it has pushed me to
learn.

I hope you have a better understanding of my light project. Check back in for
future posts where I delve into the technical aspects of living_light!

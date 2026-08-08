---
title: "High Level Service Class Design Strategy in python"
date: 2026-08-06T15:15:38-05:00
summary:
  "A simple and effective pattern for service class design in python with a
  testing strategies"
slug: "python-service-design-patterns"
Tags: []
Categories: ["design", "programming"]
DisableComments: false
Draft: true
---

This post describes very common design pattern I use when making
classes in python. I will go over the high level design, a simple example, and
how to write integration and unit tests against the pattern. The intended
audience is familiar with python basics and `pytest`. There's certainly nothing
groundbreaking about them, but these patterns are the foundation I build on when
decomposing problems in python.

## The Pattern

```python {linenos=inline}
class Service():

    def __init__(self, external_dependencies, ...):
        ...

    def public_function(self, input, ...) -> output:
        ...
```

That's all there is to it. It is the basic form any object oriented class should
follow. The constructor defines the relationship of an instance of the
class to the outside world; it should take in any sort of configuration,
external objects, or anything else required to set up the state of the object.
The public functions should implement generic interface that is unlikely to
change even if the internal implementation changes.

A good rule of thumb when trying to determine if something should be passed into
the constructor or a public method is that it should go in the constructor if
the value that would be passed in every time would be the same. Often times the
distinction is fuzzy, especially when writing the first implementation of an
interface.

## A Simple Example

The following example implements a simple service that answers yes/no questions.
`QuestionAnswerer` is the service, and `RejectionFetcher` is a dependency[^1].
The classes look like this:

```python {linenos=inline}
from abc import ABC, abstractmethod


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

```

Here's how an application could configure a `QuestionAnswerer`:

```python {linenos=inline}
import os


rejection_fetcher: RejectionFetcher
question_answerer = QuestionAnswerer(
    rejection_fetcher,
    os.environ["DEFAULT_RESPONSE"],
)
```

The application has a lot of leeway in defining what is passed into the
constructor for `QuestionAnswerer` because it can choose the implementation of
`RejectionFetcher`. In the example here it reads the default response from an
environment variable, but it could just as easily calculate it some other way.
Maybe it checks the weather and makes the default
`"No, not now. Ask again when the weather is better."` when the weather is bad.
My point is: because the constructor defines the relationship to the outside
environment, the application is free to provide it however it pleases. If
instead the class directly read an environment variable from the environment,
then every application using the class would be forced to define that variable
and have no other mechanism to set the value.

And this is how the application could make use of the constructed
`QuestionAnswerer`:

```python {linenos=inline}
question_answerer: QuestionAnswerer
question: str
answer = question_answerer.get_response(question)
```

The application logic doesn't need access to any configuration. One of the
benefits of using well defined interfaces is that the configuration can happen
far away from the core logic. It is very clear that the `request` is very
important to our application logic because it's the only thing passed into
`get_response`. Compare with a simple function as the interface for
`get_response`:

```python {linenos=inline}
get_response(
    rejection_fetcher,
    os.environ["DEFAULT_RESPONSE"],
    question
)
```

With this approach there is so more context that needs to be passed in every
time the function is called. The caller needs a reference to a
`RejectionFetcher` and the default response. This pattern tends towards bloated
function parameters with references passed into a function only to be passed
into another.

## Testing

With the design pattern well defined, up next is how to write `pytest` tests
against it.

### Integration Tests

What are integration tests? They are tests where the dependencies of the class
being tested are real implementations. The goal is to validate the behavior of
our logic when using real implementation of things. This often means that they
have to run online and talk to external services. They verify that different
modules or systems _integrate_ together.

Here's what the integration test file for `QuestionAnswerer` would look like:

```python {linenos=inline}
from pytest import fixture

DEFAULT_RESPONSE = "default response"


@fixture
def rejection_fetcher() -> RejectionFetcher:
    ...


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
```

The test has two parts, the `fixture` definitions and the tests. The `fixtures`
are responsible for building the dependencies of `QuestionAnswerer` and
contructing an instance of the class. The `question_answerer` `fixture` is
passed into the tests letting them reuse the same configuration.

The result are tests that don't have a lot of setup, making it clear what set up
is relevant for the specific case being tested.

### Unit Tests

What are unit tests? In this case, they are tests where only the behavior of the
module under test is validated (as a single _unit_). The behavior of the
dependencies are simulated through something like a `Mock` and easily set up to
verify different test cases. They should run offline, without connecting to
external services.

The breadth of what they test is much narrower than integration tests, but it is
much easier to validate all code paths.

Here's what the unit test file for `QuestionAnswerer` looks like:

```python {linenos=inline}
from unittest.mock import Mock, call

from pytest import fixture
from pytest_mock import MockerFixture


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

Similar to the integration tests, there are two parts: the `fixtures`, and the
tests. The key difference is that these tests use `Mocks` instead of using real
implementations the depndencies of `QuestionAnswerer`. `Mock` makes it easy to
simulate different behaviors and verfiy that the dependencies are used
correctly.

#### Anatomy of one unit test

Setup:

```python {linenos=inline}
def test_get_response_low_confidence_fetched_result_returns_default(
    question_answerer: QuestionAnswerer,
    rejection_fetcher: Mock,
    rejection: Mock,
):
    rejection.confidence = 0.00
```

The only test specific set up is to lower the confidence of the `Rejection`
returned by the `Mock` `RejectionFetcher`. `rejection` is already bound to be
the `return_value` of our `rejection_fetcher`'s `get_rejection` function.

This demonstrates how the `fixtures` can define the relationships between
different `Mocks`, leaving your tests responsible for only test case specific
set up.

Execute:

```python {linenos=inline}
    result = question_answerer.get_response(
        EXAMPLE_QUESTION
    )
```

Call the function that is under test and store the result.

Assert:

```python {linenos=inline}
    assert result == DEFAULT_REJECTION
    assert (
        rejection_fetcher.get_rejection.call_args
        == call(EXAMPLE_QUESTION)
    )
```

The first `assert` confirms that when our class receives a low confidence
`Rejection` that it falls back on the default rejection.

The second `assert` makes use of a functionality of `Mock` that allows you to
confirm how the `Mock` was used in your test. In this case, the statement
confirms that `get_rejection` was called with the expected arguments.

## Conclusion

I felt silly writing this because the pattern is so simple, but I've found great
use from using it as a starting point when breaking down problems.

[^1]:
    `RejectionFetcher` is also a service. I only included the abstract interface
    because the implementation details don't matter for my example.

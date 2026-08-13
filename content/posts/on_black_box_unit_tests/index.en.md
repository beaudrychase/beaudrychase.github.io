---
title: "On Black Box Unit Tests"
date: 2026-08-11T18:15:38-04:00
summary:
  "How to write stronger unit tests by verifying what's actually important."
slug: "on-black-box-unit-tests"
Tags: []
Categories: ["blog", "design", "programming"]
DisableComments: false
Draft: false
authors: ["Beaudry Chase"]
featured_image: "black_box_module.png"
---

This post is a spiritual successor to [this
previous post]({{% ref "/posts/python_service_design_pattern"%}}). It builds on
the concepts, but it should also stand on it's own.

# What is black box testing?

{{% figure src="black_box_module.png" %}} A module, represented as a... black
box{{% /figure %}}

Generally, a black box is something where the inner workings aren't understood.
They are inscrutable. Information can be gleaned from them by noticing how they
produce outputs in response to certain inputs, but how exactly the black box
derives outputs is unknown.

So, black box testing is a testing strategy where one writes the tests as though
the code under test is a black box. Good black box tests interrogate the
important functionalities provided by the public interfaces of the code without
relying on validating internal logic. Thus, they heavily focus on modeling the
relationships between inputs and outputs.

# In practice?

In practice, it is very hard to really do this. I think of true black box
testing as a kind of Platonic ideal to strive for, but reality forces us to
compromise. This is especially true with unit tests, where writing the tests
often involves doing implementation specific setup to model a test case. Often
the tests end up looking more like gray boxes than black ones.

The focus of this article is to provide strategies for navigating this grayness.
There are tradeoffs between different approaches and the goal is to make the
right ones so the tests still validate important behavior.

{{% figure src="gradient.png" %}} Gray box testing doesn't have the same ring to
it.{{% /figure %}}

## Example Code

Here's an example implementation of a service called `QuestionAnswerer` that
needs unit tests written:

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

## Unit Tests

### Dependencies Preventing True Black Box Tests

`QuestionAnswerer` is a simple service. It exposes a method called
`get_response` that under the hood forwards the `question` to a
`RejectionFetcher` service. The `RejectionFetcher` is a dependency and poses a
challenge for writing true black box unit tests. Whatever tests that are written
against this class need to be aware of how it makes use of the
`RejectionFetcher`, even though it is an internal implementation detail.

The functioning of the public `get_response` interface is dependent on what
`RejectionFetcher` returns. Users of the interface don't need to be aware of
this, but the unit tests do.

Here's what a simple unit test might look like[^1]:

```python {linenos=inline}
from pytest_mock import MockerFixture


def test_get_repsonse_high_confidence_fetched_result_returns_fetched(
    mocker: MockerFixture,
):

    fetched_rejection = "fetched rejection"
    rejection_fetcher = mocker.Mock(
        spec=RejectionFetcher
    )
    rejection = mocker.Mock(
        spec=Rejection,
        reason="fetched_rejection",
        confidence=0.90,
    )
    rejection_fetcher.get_rejection.return_value = (
        rejection
    )
    default_rejection = "default rejection"
    question_answerer = QuestionAnswerer(
        rejection_fetcher, default_rejection
    )
    question = "question"

    result = question_answerer.get_response(
        question
    )

    assert result == fetched_rejection
```

This test simply confirms that when the `RejectionFetcher` returns a result with
high confidence the response returned from `get_response` is from that value
instead of the default. This is not a true black box test because it depends on
the behavior of `RejectionFetcher`. In fact, most of the set up is just so
`get_rejection` returns the right value for this test case.

The strategy for managing this is to confirm that the class under test is using
the dependency the correct way. This usually means that asserting that the
interface was used correctly. In our case, this test needs this additional
assert:

```python {linenos=inline}
    assert (
        rejection_fetcher.get_rejection.call_args
        == call(question)
    )
```

It isn't perfect, but tests that include asserts like this are much more robust
because they confirm the module's relationship to it's dependencies. This will
surface cases where the interface has changed, or how `QuestionAnswerer` uses
`RejectionFetcher` changes.

So far, I've discussed how a test sometimes a test can't be a black box test
because it's dependencies don't allow for it. Next is how to write black box
style asserts.

### Assert External Behavior

A common issue I see in unit tests is that the asserts aren't as strong as they
should be. This often stems from asserting internal logic as a proxy for public
logic. Here's another test example:

```python {linenos=inline,hl_Lines=28}
def test_get_response_low_confidence_fetched_result_returns_default(
    question_answerer: QuestionAnswerer,
    rejection_fetcher: Mock,
    rejection: Mock,
):
    fetched_rejection = "fetched rejection"
    rejection_fetcher = mocker.Mock(
        spec=RejectionFetcher
    )
    rejection = mocker.Mock(
        spec=Rejection,
        reason="fetched_rejection",
        confidence=0.00,
    )
    rejection_fetcher.get_rejection.return_value = (
        rejection
    )
    default_rejection = "default rejection"
    question_answerer = QuestionAnswerer(
        rejection_fetcher, default_rejection
    )
    question = "question"

    result = question_answerer.get_response(
        question
    )

    assert result == question_answerer._default_answer
```

While the first test validates the behavior of `QuestionAnswerer` when
`RejectionFetcher` returns a high confidence response, this tests what happens
when `QuestionAnswerer` receives a low confidence response. The behavior
verified is that the default answer should be returned instead of the answer
from `RejectionFetcher`.

Look closely at the assert. Do the users of `QuestionAnswerer` care at all about
the value of `_default_answer`? No, they don't, but the implementation of
`QuestionAnswerer` stores the default value in that private attribute so this
test is, on the surface, correct. What users of the interface is really care
about is that the value they provided in the constructor for the default
response, is the value that was returned. This is a case where the test is
relying on internal logic in the assert, when the test has all of the
information to use a external value. This assert should be rewritten like this:

```python {linenos=inline}
    assert result == default_rejection
```

This assert validates inputs and outputs instead of internal logic. However the
class internally accounts for the default response no longer impacts the test.
This test is less likely to spurriously break[^2] while having a stronger
assert.

I hope the distinction feels clear in this example. I find that this is the most
common issue I see with unit tests. Things feel fuzzier after going through the
hassle of setting up Mocks and dealing with the complexity of real code.

## Conclusion

True black box testing is the goal but due to how code is structured, writing
tests without any awarenes of internal logic is often impossible. I hope that
these patterns are helpful when faced with these situations. Like I said above,
in real code it can be hard at a glance to see how a unit test can be improved
given how complex code is. I hope that having labels for these kinds of issues
will make identifying them easier.

[^1]:
    Astute readers of my [previous
    article]({{% ref "/posts/python_service_design_pattern"%}}) might notice the
    lack of fixtures. If I was actually writing these tests, a lot of the setup would
    be done in fixtures. For the sake of clarity and simplicity I defined everything
    in the test here.

[^2]:
    When someone renames `_default_answer` to `_default_rejection`, for
    instance.

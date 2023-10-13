from timing_utils import time_call, timed, timed_context


def test_timed_decorator():
    @timed
    def add(a, b):
        return a + b

    assert add(1, 2) == 3


def test_timed_decorator_factory():
    @timed()
    def mul(a, b):
        return a * b

    assert mul(2, 3) == 6


def test_timed_context():
    with timed_context("work"):
        assert 1 + 1 == 2


def test_time_call():
    result, seconds = time_call(lambda a, b: a + b, 2, 3)
    assert result == 5
    assert seconds >= 0

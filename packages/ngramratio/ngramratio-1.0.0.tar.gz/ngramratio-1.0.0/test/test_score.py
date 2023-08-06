import pytest

# from ngramratio import ngramratio


import sys

sys.path.insert(1, "/code")
print(sys.path)

from src.ngramratio import ngramratio  # noqa


SequenceMatcherExtended = ngramratio.SequenceMatcherExtended
s = SequenceMatcherExtended(None, "ab cde", "bcde", None)


def test_ratio():
    score = s.ratio()
    assert score == 0.8


def test_nratio_n1():
    score = s.nratio(1)
    assert score == 0.8


def test_nratio_n2():
    score = s.nratio(2)
    assert score == 0.6


def test_nratio_n3():
    score = s.nratio(3)
    assert score == 0.6


def test_nratio_n4():
    score = s.nratio(4)
    assert score == 0

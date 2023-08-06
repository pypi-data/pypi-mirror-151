#!/usr/bin/env python

"""
Class SequenceMatcherExtended:
    A class extension of SequenceMatcher for comparing pairs of sequences of any type.

Method nratio:
    A method that returns a similarity score based on matching n-grams.
"""

import difflib


def _calculate_ratio(matches, length):
    if length:
        return 2.0 * matches / length
    return 1.0


class SequenceMatcherExtended(difflib.SequenceMatcher):
    def __init__(self, isjunk=None, a="", b="", autojunk=True):
        super().__init__(None, a, b, False)

    def nratio(self, n):
        matches = sum(
            triple[-1] for triple in self.get_matching_blocks() if triple[-1] >= n
        )
        return _calculate_ratio(matches, len(self.a) + len(self.b))

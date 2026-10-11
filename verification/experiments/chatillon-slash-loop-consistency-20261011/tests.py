#!/usr/bin/env python3
"""Hand-specified controls for equality, variable lengths, masking and no paths."""
import unittest
from run_test import measure
from independent_check import dynamic_measure


def token(identifier, shape, widths=(1,), masked=False):
    return {"id": identifier, "shape": shape, "widths": list(widths), "mapping_masked": masked}


class Controls(unittest.TestCase):
    def both(self, tokens, text, fixed, targets=()):
        first = measure(tokens, text, fixed, ("first", "second"), list(targets))
        second = dynamic_measure(tokens, text, fixed, ("first", "second"), list(targets))
        self.assertEqual(first, second)
        return first

    def test_one_letter_positive(self):
        result = self.both([token("first", "A"), token("middle", "B"), token("second", "A")], "aba", {})
        self.assertEqual(result["baseline"]["count"], 1)
        self.assertEqual(result["equality"]["count"], 1)
        self.assertEqual(result["joint_slash_outputs"], [{"first": "a", "second": "a", "count": 1}])

    def test_one_letter_negative(self):
        result = self.both([token("first", "A"), token("middle", "B"), token("second", "A")], "abc", {})
        self.assertEqual(result["baseline"]["count"], 1)
        self.assertEqual(result["equality"]["count"], 0)
        self.assertEqual(result["joint_slash_outputs"], [{"first": "a", "second": "c", "count": 1}])

    def test_multicharacter_positive(self):
        result = self.both([token("first", "X", (1, 2)), token("literal", "q"),
                            token("second", "X", (1, 2))], "abqab", {"q": "q"})
        # Prefix endpoints: (ab,q,a) and (ab,q,ab), only the latter is equal.
        self.assertEqual(result["baseline"]["count"], 2)
        self.assertEqual(result["baseline"]["end_positions"], {"4": 1, "5": 1})
        self.assertEqual(result["baseline"]["end_positions"][str(len("abqab"))], 1)
        self.assertEqual(result["equality"]["count"], 1)
        self.assertEqual(result["equality"]["end_positions"], {"5": 1})
        self.assertEqual(result["equality"]["joint_slash_outputs"], [{"first": "ab", "second": "ab", "count": 1}])

    def test_multicharacter_negative(self):
        result = self.both([token("first", "X", (1, 2)), token("literal", "q"),
                            token("second", "X", (1, 2))], "abqac", {"q": "q"})
        # Two independent prefix paths, one full-endpoint path; neither is equal.
        self.assertEqual(result["baseline"]["count"], 2)
        self.assertEqual(result["baseline"]["end_positions"], {"4": 1, "5": 1})
        self.assertEqual(result["baseline"]["end_positions"][str(len("abqac"))], 1)
        self.assertEqual(result["equality"]["count"], 0)

    def test_joint_not_marginals(self):
        # Width choices produce joint (a,b), (a,ba), (ab,a). Independent
        # marginals alone cannot say which paths bind the two occurrences.
        result = self.both([token("first", "X", (1, 2)), token("second", "X", (1, 2))], "aba", {})
        self.assertEqual(result["baseline"]["count"], 3)
        self.assertEqual(result["equality"]["count"], 0)
        self.assertEqual(result["joint_slash_outputs"], [
            {"first": "a", "second": "b", "count": 1},
            {"first": "a", "second": "ba", "count": 1},
            {"first": "ab", "second": "a", "count": 1}])

    def test_masked_mapping(self):
        tokens = [token("first", "X", masked=True), token("second", "X", masked=True)]
        result = self.both(tokens, "aa", {"X": "b"})
        self.assertEqual(result["equality"]["count"], 1)
        tokens[0]["mapping_masked"] = False
        self.assertEqual(self.both(tokens, "aa", {"X": "b"})["baseline"]["count"], 0)

    def test_zero_path(self):
        result = self.both([token("first", "X"), token("literal", "q"), token("second", "X")],
                           "aba", {"q": "q"}, ("first", "second"))
        self.assertEqual(result["baseline"], {"count": 0, "projections": [{}, {}], "end_positions": {}})
        self.assertEqual(result["joint_slash_outputs"], [])
        self.assertEqual(result["equality"], {"count": 0, "projections": [{}, {}],
                                             "end_positions": {}, "joint_slash_outputs": []})

    def test_surviving_projections_and_multiplicity(self):
        result = self.both([token("first", "X"), token("left", "U", (1, 2)),
                            token("target", "U", (1, 2)), token("second", "X")], "aaaaaa", {}, ("target",))
        self.assertEqual(result["baseline"]["count"], 4)
        self.assertEqual(result["equality"]["count"], 4)
        self.assertEqual(result["equality"]["projections"], [{"a": 2, "aa": 2}])
        self.assertEqual(result["equality"]["end_positions"], {"4": 1, "5": 2, "6": 1})

    def test_n2_override(self):
        tokens = [token("first", "X"), token("n2", "N2", (1,)), token("second", "X")]
        for method in (measure, dynamic_measure):
            result = method(tokens, "aaaa", {"N2": "z"}, ("first", "second"), ["n2"], "N2", 2)
            self.assertEqual(result["baseline"]["count"], 2)
            self.assertEqual(result["equality"]["projections"], [{"a": 1, "aa": 1}])


if __name__ == "__main__":
    unittest.main(verbosity=2)

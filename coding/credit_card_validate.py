# Copyright (c) 2024 Duane R. Bailey.
# Solution to https://www.hackerrank.com/challenges/validating-credit-card-number/problem

import re
import sys
import io
import os

# These could be compiled into one regex, but it's easier to read this way.
# This also assumes that a cc either has 4 hyphen-separated groups or none.
CC_NO_SEP_REGEX = re.compile(r"""^[456][0-9]{15}$""")
CC_SEP_REGEX = re.compile(r"""^[456][0-9]{3}-[0-9]{4}-[0-9]{4}-[0-9]{4}$""")

# This regex uses the backreference to check for repeated digits.
# It matches a single digit and then 3 or more of the same digit.
FOUR_PLUS_CONSECUTIVE_DIGITS = re.compile(r"""([0-9])\1{3,}""")


# Returns true iff the cc number has 4 or more consecutive digits.
def has_more_than_three_consecutive_digits(cc):
    return FOUR_PLUS_CONSECUTIVE_DIGITS.search(cc.replace("-", "")) is not None
    # Below solution is more verbose, but it's easier to understand.
    # repeated_c = None
    # count = 0
    # for c in cc:
    #     if not c.isdigit():
    #         continue
    #     if c == repeated_c:
    #         count += 1
    #     else:
    #         repeated_c = c
    #         count = 1
    #     if count > 3:
    #         return True
    # return False


# Returns true iff the cc number is valid.
def valid_cc(cc):
    return (CC_NO_SEP_REGEX.match(cc) or CC_SEP_REGEX.match(cc)) and (
        not has_more_than_three_consecutive_digits(cc)
    )


def verify_test_samples():
    assert valid_cc("4253625879615786")
    assert valid_cc("4424424424442444")
    assert valid_cc("5122-2368-7954-3214")
    assert not valid_cc("42536258796157867")
    assert not valid_cc("4424444424442444")
    assert not valid_cc("5122-2368-7954 - 3214")
    assert not valid_cc("44244x4424442444")
    assert not valid_cc("0525362587961578")
    out_file = io.StringIO()

    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_input.txt")
    ) as in_file:
        test_lines(in_file, out_file)
    assert (
        out_file.getvalue()
        == r"""Valid
Valid
Invalid
Valid
Invalid
Invalid
"""
    )
    print("ok")


# Read the input file format described in the hackerrank problem.
def test_lines(in_file, out_file):
    n = int(in_file.readline().strip())
    for _ in range(n):
        cc = in_file.readline().strip()
        if valid_cc(cc):
            print("Valid", file=out_file)
        else:
            print("Invalid", file=out_file)


if __name__ == "__main__":
    test_lines(sys.stdin, sys.stdout)

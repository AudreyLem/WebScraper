import os
import sys

import pytest

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from src import indeed

# Tests for check_action method
@pytest.mark.parametrize(
    "action, actionList, expected",
    [
        ("scrape", ("scrape", "filter"), True),
        ("filter", ("scrape", "filter"), True),
        ("other", ("scrape", "filter"), False),
        ("scrape", (1, "filter"), False),
    ],
)
def test_check_action(action, actionList, expected):
    assert indeed.check_action(action, actionList) == expected


# Tests for getHTML method
@pytest.mark.parametrize(
    "website, status_code_expected",
    [
        ("https://au.indeed.com/jobs", 200),
    ],
)
def test_getHTML(website, status_code_expected):
    assert indeed.getHTML(website).status_code == status_code_expected
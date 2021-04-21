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


# Tests for buildingURL method
@pytest.mark.parametrize(
    "website, job, location, url_expected",
    [
        (
            "https://au.indeed.com/jobs",
            "software engineer",
            "Sydney",
            "https://au.indeed.com/jobs?q=software+engineer&l=Sydney",
        ),
        ("https://au.indeed.com/jobs", "", "", "https://au.indeed.com/jobs"),
        (
            "https://au.indeed.com/jobs",
            "software engineer",
            "",
            "https://au.indeed.com/jobs?q=software+engineer",
        ),
        (
            "https://au.indeed.com/jobs",
            "",
            "Sydney",
            "https://au.indeed.com/jobs?l=Sydney",
        ),
        (
            "https://au.indeed.com/jobs",
            "engineer",
            "Sydney CBD",
            "https://au.indeed.com/jobs?q=engineer&l=Sydney+CBD",
        ),
        (
            "https://au.indeed.com/jobs",
            "software+engineer",
            "Sydney",
            "https://au.indeed.com/jobs?q=software+engineer&l=Sydney",
        ),
    ],
)
def test_buildingURL(website, job, location, url_expected):
    assert indeed.buildingURL(website, job, location) == url_expected
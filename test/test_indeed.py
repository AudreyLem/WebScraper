import os
import sys

import pytest

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from src import indeed


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
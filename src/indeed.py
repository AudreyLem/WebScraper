# CommandLine App using Python 3.6+ to scrap information from Indeed.com
import sys
from argparse import ArgumentParser
from typing import List, Optional

import typer

WebScraper_Parser = typer.Typer()
actionList = ("scrape", "filter")


@WebScraper_Parser.command()
def indeed(
    action: str,
    website: Optional[str] = "https://indeed.com",
    job: Optional[List[str]] = None,
    location: Optional[List[str]] = None,
    salary: Optional[List[str]] = None,
    save: Optional[str] = "jobs.json",
    no_cache: Optional[bool] = False,
) -> str:
    if action not in actionList:
        print(
            "This action",
            action,
            " is not available.",
            "\nActions available: ",
            actionList,
        )
        sys.exit()
    else:
        print(
            "action: ",
            action,
            "\nwebsite: ",
            website,
            "\njobs:",
            job,
            "\nlocations:",
            location,
            "\nsalaries:",
            salary,
            "\nsave:",
            save,
            "\nno-cache:",
            no_cache,
        )


if __name__ == "__main__":
    WebScraper_Parser()

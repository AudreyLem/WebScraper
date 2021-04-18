# CommandLine App using Python 3.6+ to scrap information from Indeed.com
import sys
from argparse import ArgumentParser
from typing import List, Optional

import requests
import typer

WebScraper_Parser = typer.Typer()
actionList = ("scrape", "filter")


def check_action(action: str, actionList: List[str]) -> bool:
    """
    Parameters:
        action (str): Name of the action
        actionList (List[str]): Names of actions available

        Returns:
        bool: is action in ActionList or not
    """

    if action not in actionList:
        print(
            "This action",
            action,
            " is not available.",
            "\nActions available: ",
            actionList,
        )
        return False
    else:
        return True


@WebScraper_Parser.command()
def indeed_scrape(
    action: str,
    website: Optional[str] = "https://au.indeed.com/jobs",
    job: Optional[List[str]] = None,
    location: Optional[List[str]] = None,
    salary: Optional[List[str]] = None,
    save: Optional[str] = "jobs.json",
    no_cache: Optional[bool] = False,
) -> str:
    """
    Parameters:
        action (str): scrape or filter,
        website (str): Optional parameter to set the website to be scraped. Default value: "https://au.indeed.com/jobs",
        job (List[str]): Optional parameter to set the jobs to filter,
        location (List[str]): Optional parameter to set the locations to filter,
        salary (List[str]): Optional parameter to set the salaries to filter,
        save (str): Optional parameter to set the file where data will be stored. Default value: "jobs.json",
        no_cache(bool): Optional parameter to indicate if we use cached data or not. Default value = False,

        Returns:
        str: data or filename in which data have been saved (if --save parameter was used)
    """

    # Docstrings
    # print(indeed_scrape.__doc__)

    if check_action(action, actionList):
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

        # Retrieving HTML content from 'website' url
        page = requests.get(website)

        # Debug: To print status_code to know if the GET command worked
        # print(page.status_code)

        # print(page.content)
        return page.status_code
    else:
        sys.exit()


if __name__ == "__main__":
    WebScraper_Parser()

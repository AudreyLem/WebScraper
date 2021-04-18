# CommandLine App using Python 3.6+ to scrap information from Indeed.com
import sys, glob, os
from argparse import ArgumentParser
from typing import List, Optional
from pathlib import Path

import requests
import typer

# path (with fileName with extension)
path = os.path.realpath(__file__)
# File Name (with extension)
fileNameWithoutExtension = Path(path).stem
# src directory
currentdir = os.path.dirname(path)
# WEBSCRAPER directory
parentdir = os.path.dirname(currentdir)
# CacheFiles directory
cacheFilesDirectory = str(Path(parentdir + "\cacheFiles"))

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


def getHTML(website) -> requests.Response:
    """
    Parameters:
        website (str): URL of the website from which we want to retrieve HTNL content

        Returns:
        requests.Response: HTML content
    """
    return requests.get(website)


def isWebsiteCached(websiteName, pathCacheFiles) -> bool:
    """
    Parameters:
        websiteName (str): name of the website

        Returns:
        bool: is cache file already exist or not-
    """
    cacheFiles = glob.glob(pathCacheFiles + "/*" + websiteName + ".html")
    return len(cacheFiles) == 1


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

        # print(page.content)
        if action == "scrape":
            print("Scraping...")

            # if we should use cafe file
            if not (no_cache):
                # if cachefile does not exist, we create it
                if not (isWebsiteCached(fileNameWithoutExtension, cacheFilesDirectory)):
                    # Retrieving HTML content from 'website' url
                    page = getHTML(website)
                    # Creating .html cache file
                    with open(
                        cacheFilesDirectory + "/" + fileNameWithoutExtension + ".html",
                        mode="w",
                    ) as file:
                        file.write(str(page.content))

                # Scrape in cache file

            # if we should not use cache file
            else:
                # Retrieving HTML content from 'website' url
                page = getHTML(website)

        elif action == "filter":
            # TODO
            print("Filtering...")
        else:
            # Do nothing
            print("Nothing")
        # return page.status_code
    else:
        sys.exit()


if __name__ == "__main__":
    WebScraper_Parser()

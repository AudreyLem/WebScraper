# CommandLine App using Python 3.6+ to scrap information from Indeed.com
import sys, glob, os
from argparse import ArgumentParser
from typing import List, Optional
from pathlib import Path
from bs4 import BeautifulSoup

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


def buildingURL(website, job, location) -> str:
    """
    Parameters:
        website (str): URL with no filter
        job (str): job to add to the URL
        location (str): location to add to the URL

        Returns:
        str: URL with filters added
    """
    url = website
    if job:
        url = url + "?q=" + job.replace(" ", "+")
    if location:
        if job:
            url = url + "&l=" + location.replace(" ", "+")
        else:
            url = url + "?l=" + location.replace(" ", "+")
    return url


@WebScraper_Parser.command()
def indeed_scrape(
    action: str,
    website: Optional[str] = "https://au.indeed.com/jobs",
    job: Optional[str] = None,
    location: Optional[str] = None,
    salary: Optional[str] = None,
    save: Optional[str] = "jobs.json",
    no_cache: Optional[bool] = False,
) -> str:
    """
    Parameters:
        action (str): scrape or filter,
        website (str): Optional parameter to set the website to be scraped. Default value: "https://au.indeed.com/jobs",
        job (str): Optional parameter to set the job to filter,
        location (str): Optional parameter to set the location to filter,
        salary (str): Optional parameter to set the salary to filter (equal or greater),
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
            # Building URL ('website' url + location + job)
            url = buildingURL(website, job, location)
            

            # if we should use cache file
            if not (no_cache):
                # if cachefile does not exist, we create it
                if not (isWebsiteCached(fileNameWithoutExtension, cacheFilesDirectory)):
                    # Retrieving HTML content from url
                    page = getHTML(url)
                    # Creating .html cache file
                    with open(
                        cacheFilesDirectory + "/" + fileNameWithoutExtension + ".html",
                        mode="w",
                    ) as file:
                        file.write(str(page.content))
                    print("New cache file ",cacheFilesDirectory + "/" + fileNameWithoutExtension + ".html created.")
                # if cachefile does exist, we overwrite it
                else:
                    # Cache file does already exists --> Nothing to do
                    print("Nothing done: cache file ",cacheFilesDirectory + "/" + fileNameWithoutExtension + ".html exists already.")

            # if we should not use cache file
            else:
                print("--no-cache...")
                # Retrieving HTML content from url
                page = getHTML(url)
                # Overwriting
                with open(
                    cacheFilesDirectory + "/" + fileNameWithoutExtension + ".html",
                    mode="r+",
                ) as file:
                    data = file.read()
                    data = str(page.content)
                    file.write(data)
                print("Cache file ",cacheFilesDirectory + "/" + fileNameWithoutExtension + ".html overwritten.")
        elif action == "filter":
            # TODO
            print("Filtering...")
            # Check if HTML cache file exists and create it with fresh data if it does not exist yet.
            if not (isWebsiteCached(fileNameWithoutExtension, cacheFilesDirectory)):
                indeed_scrape(
                    action,
                    websiten,
                    jobn,
                    location,
                    salary,
                    save,
                    no_cache,
                )
            soup = BeautifulSoup(page.content, 'html.parser')
            
        else:
            # Do nothing
            print("Nothing")
        # return page.status_code
    else:
        sys.exit()


if __name__ == "__main__":
    WebScraper_Parser()

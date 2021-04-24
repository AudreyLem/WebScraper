# CommandLine App using Python 3.6+ to scrap information from Indeed.com
import sys, glob, os, json
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


def getHTML(website: str) -> requests.Response:
    """
    Parameters:
        website (str): URL of the website from which we want to retrieve HTNL content

        Returns:
        requests.Response: HTML content
    """
    return requests.get(website)


def doesFileExist(websiteName: str, pathCacheFiles: str, extension: str) -> bool:
    """
    Parameters:
        websiteName (str): name of the website
        pathCacheFiles (str): name of the path to the cache files folder
        extension (str): extension of the file (HTML, json, etc.)

        Returns:
        bool: is cache file already exist or not
    """
    cacheFiles = glob.glob(pathCacheFiles + "/*" + websiteName + "." + extension)
    return len(cacheFiles) == 1


def buildingURL(website: str, job: str, location: str) -> str:
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


def prettyStr(stringInput: str) -> str:
    """
    Parameters:
        stringInput (str): string to make pretty

        Returns:
        str: pretty string
    """
    strOutput = " ".join(stringInput.strip().replace("\n", "").split())
    return strOutput


@WebScraper_Parser.command()
def indeed_scrape(
    action: str,
    website: Optional[str] = "https://au.indeed.com/jobs",
    job: Optional[str] = None,
    location: Optional[str] = None,
    rating: Optional[float] = 0,
    salary: Optional[float] = 0,
    save: Optional[str] = None,
    no_cache: Optional[bool] = False,
):
    """
    Parameters:
        action (str): scrape or filter,
        website (str): Optional parameter to set the website to be scraped. Default value: "https://au.indeed.com/jobs",
        job (str): Optional parameter to set the job to filter,
        location (str): Optional parameter to set the location to filter,
        rating (float): Optional parameter to set the rating to filter (equal or greater). Default value: 0,
        salary (float): Optional parameter to set the salary to filter (equal or greater). Default value: 0,
        save (str): Optional parameter to set the file where data will be stored,
        no_cache(bool): Optional parameter to indicate if we use cached data or not. Default value = False,
    """

    # Docstrings
    # print(indeed_scrape.__doc__)

    if check_action(action, actionList):
        # print(
        #     "action: ",
        #     action,
        #     "\nwebsite: ",
        #     website,
        #     "\njob:",
        #     job,
        #     "\nlocation:",
        #     location,
        #     "\nrating:",
        #     str(rating),
        #     "\nsalary:",
        #     str(salary),
        #     "\nsave:",
        #     save,
        #     "\nno-cache:",
        #     no_cache,
        # )

        if action == "scrape":
            print("Scraping...")
            # Building URL ('website' url + location + job)
            url = buildingURL(website, job, location)

            # if we should use cache file
            if not (no_cache):
                # if cachefile does not exist, we create it
                if not (
                    doesFileExist(fileNameWithoutExtension, cacheFilesDirectory, "html")
                ):
                    # Retrieving HTML content from url
                    page = getHTML(url)
                    # To get data structure to represent a parsed HTML
                    soup = BeautifulSoup(page.content, "html.parser")
                    # Creating .html cache file
                    with open(
                        cacheFilesDirectory + "/" + fileNameWithoutExtension + ".html",
                        mode="w",
                        encoding="utf-8",
                    ) as file:
                        file.write(soup.prettify())
                    print(
                        "New cache file ",
                        cacheFilesDirectory
                        + "/"
                        + fileNameWithoutExtension
                        + ".html created.",
                    )
                # if cachefile does exist
                else:
                    # Cache file already exists --> Nothing to do
                    print(
                        "Nothing done: cache file ",
                        cacheFilesDirectory
                        + "/"
                        + fileNameWithoutExtension
                        + ".html exists already.",
                    )

            # if we should not use cache file
            else:
                print("--no-cache...")
                # Retrieving HTML content from url
                page = getHTML(url)
                # To get data structure to represent a parsed HTML
                soup = BeautifulSoup(page.content, "html.parser")
                # Overwriting
                with open(
                    cacheFilesDirectory + "/" + fileNameWithoutExtension + ".html",
                    mode="w",
                    encoding="utf-8",
                ) as file:
                    file.write(soup.prettify())
                print(
                    "Cache file ",
                    cacheFilesDirectory
                    + "/"
                    + fileNameWithoutExtension
                    + ".html overwritten.",
                )
        elif action == "filter":
            print("Filtering...")

            # Cleaning JSON file
            Path(cacheFilesDirectory + "\jobs.json").unlink(missing_ok=True)

            # Check if HTML cache file exists and create it with fresh data if it does not exist yet.
            if not (
                doesFileExist(fileNameWithoutExtension, cacheFilesDirectory, "html")
            ):
                indeed_scrape(
                    action,
                    website,
                    job,
                    rating,
                    location,
                    salary,
                    save,
                    no_cache,
                )
            with open(
                cacheFilesDirectory + "/" + fileNameWithoutExtension + ".html",
                mode="r",
                encoding="utf-8",
            ) as file:
                # To get data structure to represent a parsed HTML file
                soup = BeautifulSoup(file, "html.parser")
                # Get all jobs as set of PageElement
                jobs = soup.find_all(
                    "div", class_="jobsearch-SerpJobCard unifiedRow row result"
                )

                for job in jobs:
                    # Retrieve PageElements
                    jobTitle_PageElement = job.find(
                        "a", class_="jobtitle turnstileLink"
                    )
                    jobCompany_PageElement = job.find("span", class_="company")
                    jobLocation_PageElement = job.find(
                        "span", class_="location accessible-contrast-color-location"
                    )
                    jobRating_PageElement = job.find("span", class_="ratingsContent")
                    jobSalary_PageElement = job.find("span", class_="salaryText")

                    # Skipping if no jobTitle
                    if jobTitle_PageElement == None:
                        continue
                    else:
                        jobTitle = " ".join(
                            jobTitle_PageElement.text.strip().replace("\n", "").split()
                        )

                    # Convert to a pretty string all PageElements
                    if jobCompany_PageElement == None:
                        jobCompany == "?"
                    else:
                        jobCompany = prettyStr(jobCompany_PageElement.text)
                    if jobLocation_PageElement == None:
                        jobLocation = "?"
                    else:
                        jobLocation = prettyStr(jobLocation_PageElement.text)
                    if jobRating_PageElement == None:
                        jobRating = 0
                    else:
                        jobRating = float(prettyStr(jobRating_PageElement.text.strip()))
                    if jobSalary_PageElement == None:
                        jobSalaryOriginal = "?"
                        jobSalaryFloat = -1.0
                    else:
                        jobSalaryOriginal = prettyStr(
                            jobSalary_PageElement.text.strip()
                        )
                        jobSalary = prettyStr(jobSalary_PageElement.text.strip())
                        if jobSalaryOriginal.find("a year") != -1:
                            if jobSalaryOriginal.find("-") != -1:
                                jobSalary = jobSalary[: jobSalary.find("-") - 1]
                            jobSalaryFloat = float(
                                jobSalary.replace("$", "")
                                .replace(" a year", "")
                                .replace(",", "")
                            )
                        elif jobSalaryOriginal.find("a month") != -1:
                            if jobSalaryOriginal.find("-") != -1:
                                jobSalary = jobSalary[: jobSalary.find("-") - 1]
                            jobSalaryFloat = (
                                float(
                                    jobSalary.replace("$", "")
                                    .replace(" a month", "")
                                    .replace(",", "")
                                )
                                * 12  # 12 months a year
                            )
                        elif jobSalaryOriginal.find("an hour") != -1:
                            if jobSalaryOriginal.find("-") != -1:
                                jobSalary = jobSalary[: jobSalary.find("-") - 1]
                            jobSalaryFloat = (
                                float(
                                    jobSalary.replace("$", "")
                                    .replace(" an hour", "")
                                    .replace(",", "")
                                )
                                * 40  # 40h/a week
                                * 52  # 52 weeks/a year
                            )
                        else:
                            jobSalaryFloat = -1.0

                    # Filtering on jobRating
                    if jobRating >= rating and (
                        jobSalaryFloat >= salary or jobSalaryFloat == -1.0
                    ):
                        if save == None:
                            print(
                                "Job title:",
                                jobTitle,
                                ", Company:",
                                jobCompany,
                                ", Location:",
                                jobLocation,
                                ", Rating: ",
                                str(jobRating),
                                ", Salary:",
                                jobSalaryOriginal,
                            )
                        else:
                            # Check if json file exists and create it if it does not exist yet.
                            if not (doesFileExist("jobs", cacheFilesDirectory, "json")):
                                with open(
                                    cacheFilesDirectory + "\jobs.json", mode="w"
                                ) as file:
                                    file.write("")
                                print(
                                    "New JSON file",
                                    cacheFilesDirectory + "\jobs.json created.",
                                )

                            # Print job's info in json format into json file
                            with open(
                                cacheFilesDirectory + "\jobs.json", mode="a"
                            ) as file:
                                data = json.dumps(
                                    {
                                        "Job title:": jobTitle,
                                        ", Company:": jobCompany,
                                        ", Location:": jobLocation,
                                        ", Rating: ": str(jobRating),
                                        ", Salary:": jobSalaryOriginal,
                                    },
                                    indent=4,
                                )
                                file.write(data)

        else:
            # Do nothing
            print("Nothing")
    else:
        sys.exit()


if __name__ == "__main__":
    WebScraper_Parser()

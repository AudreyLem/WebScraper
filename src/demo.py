import glob
import os
from pathlib import Path

# path (with fileName with extension)
path = os.path.realpath(__file__)
# File Name (with extension)
fileNameWithoutExtension = Path(path).stem
# src directory
currentdir = os.path.dirname(path)
# WEBSCRAPER directory
parentdir = os.path.dirname(currentdir)
# CacheFiles directory
cacheFilesDirectory = Path(parentdir + "\cacheFiles")

print(str(cacheFilesDirectory))


def isWebsiteCached(websiteName) -> bool:
    cacheFiles = glob.glob(str(parentdir) + "/cacheFiles/*" + websiteName + "*.html")
    # print(parentdir)
    return len(cacheFiles) > 0


print(isWebsiteCached("indeed"))

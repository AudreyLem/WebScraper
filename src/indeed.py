# CommandLine App using Python 3.6+ to scrap information from Indeed.com
import argparse
import sys

# Parser creation
WebScraper_Parser = argparse.ArgumentParser(description='Scrap jobs from Indeed.com')

# Arguments definition
WebScraper_Parser.add_argument('Command', metavar='command', type=str, help='scrape to scrap Indeed.com / filter to add filter(s)')

# Execute the parse_args() method
args = WebScraper_Parser.parse_args()

command = args.Command
commandList = ('scrape','filter')

if command not in commandList:
    print('This command is not available:', command,'\nType -h to see how to use', __file__)
    sys.exit()


print(command)
# WebScraper
Capstone project of PyCap learning

Usage: indeed.py [OPTIONS] ACTION

  Parameters:     
  action (str): scrape or filter,     
  website (str): Optional parameter to set the website to be scraped. Default value: "https://au.indeed.com/jobs",     
  job (str): Optional parameter to set the job to filter,     
  location (str): Optional parameter to set the location to filter, 
  rating (float): Optional parameter to set the rating to filter (equal or greater). Default value: 0,     
  salary (float): Optional parameter to set the salary to filter (equal or greater). Default value: 0,  
  save (str): Optional parameter to set the file where data will be stored,     
  no_cache(bool): Optional parameter to indicate if we use cached data or not. Default value = False,

Arguments:
  ACTION  [required] ('scrape' or 'filter')

Options:
  
  --website TEXT                  [default: https://au.indeed.com/jobs]
  --job TEXT
  --location TEXT
  --rating FLOAT                  [default: 0]
  --salary FLOAT                  [default: 0]
  --save TEXT
  --no-cache / --no-no-cache      [default: False]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

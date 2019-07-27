from json import load
from pandas import read_csv
import os
import urllib
from utils import folder_maker, year_to_session
from typing import Dict, Optional


def file_scraper(url, file_name: str) -> bool:
    """
    Makes a file with the records of how the vote happened. Vote number corresponds to natural not positive scale.
    Returns a boolean where True corresponds to a successful scrape and False to a file not being found
    (Only been tested from 2000 onwards)
    """
    try:
        read_csv(url).to_csv(file_name, encoding='utf-8')
    except urllib.error.HTTPError as err:
        if err.code == 404:  # Vote not present in raw_data
            print(f'{url} Not Found')
            return False
        elif err.code == 429:  # its retrying the server
            print(f'  -server issue at {url}')
            file_scraper(url, file_name)
        else:  # errors I have not yet encountered
            print('Other Error Encountered for {url}')
    return True


def year_scraper(year: int, chamber: str, issues: Optional[Dict[str, str]]) -> None:
    """ Function to scrape through all votes for one year in one chamber """
    print_chamber = chamber.capitalize() + ('ouse' if chamber == 'h' else 'enate')
    print(f'======== Scraping for {print_chamber} {year} Beginning ========')
    path = f'data/raw_data/{year}/{chamber}'
    folder_maker(path)
    session = year_to_session(year)
    exit_tally = 0
    n = 0
    while exit_tally < 10:
        if n % 100 == 0:
            print(f'-------- {n} files have been processed --------')
        file = f'data/raw_data/{year}/{chamber}/{n}.csv'
        if not os.path.exists(file):
            url = f'https://www.govtrack.us/congress/votes/{session}-{year}/{chamber}{n+1}/export/csv'
            if issues and url in issues:
                print(f'previous issue at: {url}')
                print('See issues.json for comment. Skipping')
                continue
            exit_tally = 0 if file_scraper(url, file) else exit_tally + 1
        n += 1
    print(f'======== Scraping for {print_chamber} {year} Complete ========')


def scraper(start: int, end: int, issues: Optional[str] = None) -> None:
    """
    Function to scrape house and senate votes for years
    start, end: the starting and ending years for scraping, can go in either order
    issues: the path for issues.json dict with known urls with issues
    """
    if issues:
        with open(issues, 'r') as f:
            issues = load(f)
    step = 1 if start <= end else -1
    print(f'============ Starting Scraping for {start}-{end} ============')
    for i in range(start, end + step, step):
        year_scraper(i, 'h', issues)
        year_scraper(i, 's', issues)
    print(f'============ Finished Scraping for {start}-{end} ============')


if __name__ == '__main__':
    start_year = int(input('Start Scraping from (year): '))
    end_year = int(input('to (year) : '))
    known_issues = input('issues.json path (leave blank if you do not wish to use it)')
    scraper(start_year, end_year, known_issues)

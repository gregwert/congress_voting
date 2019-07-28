from argparse import ArgumentParser
from json import load
from os.path import exists
from typing import Optional
from urllib.error import HTTPError

from pandas import DataFrame, read_csv
from pandas.errors import ParserError

from utils import folder_maker, year_to_session


def scraper(start: int, end: int, issues: Optional[str] = None, out: str = 'data') -> None:
    """
    Function to scrape house and senate votes for years
    start, end: the starting and ending years for scraping, can go in either order
    issues: the path for issues.json dict with known urls with issues
    out: path for where the data will be saved
    """
    if issues:
        with open(issues, 'r') as f:
            print(f'Loading: {issues}')
            issues = load(f)
    step = 1 if start <= end else -1
    print(f'============ Starting Scraping for {start}-{end} ============')
    for i in range(start, end + step, step):
        year_scraper(i, 'h', issues, out)
        year_scraper(i, 's', issues, out)
    print(f'============ Finished Scraping for {start}-{end} ============')


def year_scraper(year: int, chamber: str, issues: Optional[dict], out: str) -> None:
    """ Function to scrape through all votes for one year in one chamber """
    print_chamber = chamber.capitalize() + ('ouse' if chamber == 'h' else 'enate')
    print(f'======== Scraping for {print_chamber} {year} Beginning ========')
    path = f'{out}/raw_data/{year}/{chamber}'
    folder_maker(path)
    session = year_to_session(year)
    exit_tally, n = 0, 0
    while exit_tally < 10:
        if n % 100 == 0:
            print(f'-------- {n} files have been processed --------')
        url = f'https://www.govtrack.us/congress/votes/{session}-{year}/{chamber}{n + 1}/export/csv'
        file = f'data/raw_data/{year}/{chamber}/{n}.csv'
        n += 1
        if not exists(file):
            if issues and url in issues:
                print(f'previous issue at: {url}')
                print('See issues.json for comment. Skipping')
                continue
            exit_tally = 0 if page_scraper(url, file) else exit_tally + 1
    print(f'======== Scraping for {print_chamber} {year} Complete ========')


def page_scraper(url, file_name: str) -> bool:
    """
    Makes a file with the records of how the vote happened. Vote number corresponds to natural not positive scale.
    Returns a boolean where True corresponds to a successful scrape and False to a file not being found
    (Only been tested from 2000 onwards)
    """
    try:
        df = parsing_robust_scraping(url)
        df.to_csv(file_name, encoding='utf-8')
    except HTTPError as err:
        if err.code == 404:  # Vote not present in raw_data
            print(f'{url} Not Found')
            return False
        elif err.code == 429:  # its retrying the server
            print(f'  -server issue at {url}')
            page_scraper(url, file_name)
        else:  # errors I have not yet encountered
            print(f'Other Error Encountered for {url}')
            print(err)
    return True


def parsing_robust_scraping(url: str, header_len: int = 1) -> DataFrame:
    """ Deals with irregular headers and returns resulting DataFrame """
    try:
        df = read_csv(url, header=[i for i in range(header_len)])
        if header_len > 1:  # on parsing errors the title is spread over more than one line
            df.columns = df.columns.map('|'.join).str.strip('|')  # thus is we encounter one we merge the lines
        return df
    except ParserError:
        return parsing_robust_scraping(url, header_len+1)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--start', help='the year you want to start scraping', type=int, required=True)
    parser.add_argument('--end', help='the year you want to stop scraping', type=int, required=True)
    parser.add_argument('--issues', help='the location of the issue.json ; useful for avoiding known problematic files',
                        type=str, required=False, default=None)
    parser.add_argument('--out', help='the location where you want to store the scraped data',
                        type=str, required=False, default='data/')
    args = parser.parse_args()
    scraper(args.start, args.end, args.issues, args.out)

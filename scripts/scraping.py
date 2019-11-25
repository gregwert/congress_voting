from argparse import ArgumentParser

from congress_voting.scraper import scraper

parser = ArgumentParser()
parser.add_argument('--start', help='the year you want to start scraping', type=int, required=True)
parser.add_argument('--end', help='the year you want to stop scraping', type=int, required=True)
parser.add_argument('--issues', help='the location of the issue.json ; useful for avoiding known problematic files',
                    type=str, required=False, default=None)
parser.add_argument('--out', help='the location where you want to store the scraped data',
                    type=str, required=False, default='data/')
args = parser.parse_args()
scraper(args.start, args.end, args.issues, args.out)

from json import dump, load
from os import makedirs
from os.path import exists


def folder_maker(path: str) -> None:
    """" Makes a new folder in the inventory corresponding to the year and chamber of votes """
    if not exists(path):
        print(f'Making folder: {path}')
        makedirs(path)


def issue_update(issue_dict: str, url:str, issue: str, comment: str):
    with open(issue_dict, 'r') as f:
        d = load(f)
    entry = {url: {'issue': issue, 'comments': comment}}
    d.update(entry)
    with open(issue_dict, 'w') as f:
        dump(d, f)

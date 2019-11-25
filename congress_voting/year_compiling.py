from functools import reduce
from os import listdir

from pandas import DataFrame, read_csv, read_table, merge

from congress_voting.utils import folder_maker


# TODO: consolidate into single class
# TODO: document


def read_file(file: str) -> DataFrame:
    df, vote = read_csv(file, header=1), read_table(file).columns[0]
    df = df.rename(index=str, columns={'vote': vote})
    return df[['person', 'name', 'state', 'district', 'party', vote]]


def read_year(year: int, chamber: str, data_loc: str) -> DataFrame:
    path = f'{data_loc}/raw_data/{year}/{chamber}/'
    dfs = (read_file(path + f) for f in listdir(path))
    return reduce(lambda l, r: merge(l, r, on=['person', 'name', 'state', 'district', 'party'], how='outer'), dfs)


def save_data(start, end, data_loc: str = '', out: str = 'data'):
    step = 1 if start <= end else -1
    years = range(start, end + step, step)
    year_gen = ((year, read_year(year, 'h', data_loc), read_year(year, 's', data_loc)) for year in years)
    for year, house, senate in year_gen:
        path = f'{out}/yearly_records/{year}/'
        folder_maker(path)
        path += str(year)
        house.to_csv(f'{path}_h_votes.csv', index=False)
        senate.to_csv(f'{path}_s_votes.csv', index=False)

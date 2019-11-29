from functools import reduce
from os import listdir
from typing import Iterable, Union

from numpy import concatenate
from pandas import DataFrame, Index, Series, merge, read_csv, read_table

from congress_voting.utils import folder_maker, session_to_years, year_pair

# TODO: consolidate into single class
# TODO: document

id_columns = ['person', 'name', 'state', 'district', 'party']
yes_options = ['Aye', 'Yea', 1]


def read_file(file: str) -> DataFrame:
    df, vote = read_csv(file, header=1), read_table(file).columns[0]
    df = df.rename(index=str, columns={'vote': vote})
    return df[id_columns + [vote]]


def read_year(year: int, chamber: str, data_loc: str) -> DataFrame:
    path = f'{data_loc}/raw_data/{year}/{chamber}/'
    dfs = (read_file(path + file) for file in listdir(path))
    return reduce(lambda l, r: merge(l, r, on=id_columns, how='outer'), dfs)


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


def process_csv(file: str, chamber: str) -> DataFrame:
    def name_clean(name: str) -> str:
        return name.split('[')[0].replace('Sen.' if chamber is 's' else 'Rep.', '').strip()

    df = read_csv(file)
    df.name = df.name.apply(name_clean)
    return df


def load_data(chamber: str, session: int = None, year: int = None, data_loc: str = ''):
    if session is None and year is None:
        raise ValueError("Must provide a value for either 'year' or 'session'")
    elif session is not None and year is not None:
        raise ValueError("Cannot provide values for both 'session' and 'year'. Must only provide one")
    years = session_to_years(session) if session is not None else year_pair(year)
    df = [process_csv(f'{data_loc}/yearly_records/{y}/{y}_{chamber}_votes.csv', chamber) for y in years]
    df = merge(left=df[0], right=df[1], on=id_columns, how='outer')
    return df


def process_data(data: DataFrame) -> DataFrame:
    data = data.copy().fillna('')
    data = consolidate_duplicates(data=data)
    vote_columns = get_vote_columns(data=data)
    data[vote_columns] = data[vote_columns].apply(yes_votes)
    return data


def vote_possibilities(data: DataFrame, columns: Iterable[Union[str, int]] = None) -> set:
    if columns is None:
        columns = get_vote_columns(data=data)
    return set(concatenate([data[vote].unique() for vote in columns]))


def get_vote_columns(data: DataFrame) -> Index:
    return data.columns[data.columns.isin(id_columns) == False]


def yes_votes(vote: Series) -> Series:
    def yes_check(choice: str):
        return 1 if choice in yes_options else 0

    return vote.apply(yes_check)


def consolidate_duplicates(data: DataFrame) -> DataFrame:
    person_counts = data.person.value_counts()
    duplicates = person_counts.loc[person_counts > 1].index
    if len(person_counts) == 0:
        return data
    else:
        duplicates = data.loc[data.person.isin(duplicates)]
        consolidated = duplicates.groupby(['person']).max().reset_index()
        return data.drop(duplicates.index).append(consolidated).reset_index(drop=True)

from typing import Tuple


def year_to_session(year: int) -> int:
    """ Maps the year to the session of congress """
    return int((year - 1788 + year % 2) / 2)


def session_to_years(session: int) -> Tuple[int, int]:
    year = int(2 * session + 1788)
    return year - 1, year


def year_pair(year: int) -> Tuple[int, int]:
    return (year - 1, year) if year % 2 == 0 else (year, year + 1)

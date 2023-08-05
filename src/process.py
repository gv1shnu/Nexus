from src.db_handler import DBHandler
from datetime import date


def process(query: str) -> tuple:
    """
    Processes a query by checking the search results database.
    Takes a query as input and checks the search results database using the DBHandler class.

    Args:
        query (str): The user's query.

    Returns:
        list or None: The search results obtained from the database or web scraping, or None if no results are found.
    """
    dbhandler = DBHandler()
    x = dbhandler.query(req=query)

    if x:  # entry exists
        if get_diff_dates(date1=x['date'], date2=str(date.today())) >= 7:  # is older than a week
            return dbhandler.update(entry=x)
        else:  # is fresh
            return x['count'], x['time'], x['pages']
    else:
        print("\033[92m No entry found.\n Scraping...")
        return dbhandler.insert(req=query)


def get_diff_dates(date1: str, date2: str) -> int:
    """
    Get difference in number of days between two dates

    Args:
        date1 (str): first date in Y-M-D format
        date2 (str): second date in Y-M-D format

    Returns: an integer
    """
    t1 = date1.split('-')
    r1 = (int(t1[0]) - 1) * 365 + int(t1[1]) * 12 + int(t1[2])
    t2 = date2.split('-')
    r2 = (int(t2[0]) - 1) * 365 + int(t2[1]) * 12 + int(t2[2])

    return r2 - r1

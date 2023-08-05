from src.db_handler import DBHandler
from datetime import date
import selenium


def process(query: str, driver_service: selenium.webdriver.chrome.service.Service) -> list:
    """
    Processes a query by checking the search results database.
    Takes a query as input and checks the search results database using the DBHandler class.

    Args:
        query (str): The user's query.
        driver_service (selenium.webdriver.chrome.service.Service): Passing along driver service.

    Returns:
        list or None: The search results obtained from the database or web scraping, or None if no results are found.
    """
    dbhandler = DBHandler()
    x = dbhandler.query(req=query)
    if x:  # entry exists
        if get_diff_dates(date1=x['date'], date2=str(date.today())) >= 7:  # is older than a week
            y = dbhandler.update(entry=x, ds=driver_service)
            return y
        else:  # is fresh
            return x['results']
    else:
        print("\033[92m No entry found.\n Scraping...")
        y = dbhandler.insert(req=query, ds=driver_service)
        print("\033[92mDone")
        return y


def get_diff_dates(date1: str, date2: str) -> int:
    t1 = date1.split('-')
    r1 = (int(t1[0]) - 1) * 365 + int(t1[1]) * 12 + int(t1[2])
    t2 = date2.split('-')
    r2 = (int(t2[0]) - 1) * 365 + int(t2[1]) * 12 + int(t2[2])

    return r2 - r1

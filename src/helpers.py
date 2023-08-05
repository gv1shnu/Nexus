from src.db_handler import DBHandler


def process(query):
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
    if not x:
        print("\033[92m No entry found.\n Scraping...\033[92m")
        x = dbhandler.insert(req=query)
    return x

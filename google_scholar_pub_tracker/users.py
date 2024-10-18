from scholarly import scholarly
import sys


def get_first_author(author_name: str) -> str:
    # Retrieve the author's data, fill-in, and print
    # Get an iterator for the author results
    search_query = scholarly.search_author(author_name)
    # Retrieve the first result from the iterator
    first_author_result = next(search_query)
    return first_author_result


def get_author_by_google_scholar_id(google_scholar_id: str) -> str:
    pg = scholarly.ProxyGenerator()

    if not pg.FreeProxies():
        print("FreeProxies fail")
        sys.exit()
    scholarly.use_proxy(pg)

    google_scholar_candidates = []

    try:
        result = scholarly.search_author_id(google_scholar_id)
        print(result)
        google_scholar_candidates.append(result)
    except Exception as e:
        print(f"Could not query google with id")

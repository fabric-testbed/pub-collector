from scholarly import scholarly
from scholarly import ProxyGenerator
import sys


def get_first_author(author_name):
    # Retrieve the author's data, fill-in, and print
    # Get an iterator for the author results
    results = scholarly.search_author(author_name)
    # print(list(results))
    # Retrieve the first result from the iterator
    first_author_result = next(results)
    return first_author_result


def get_author_by_google_scholar_id(google_scholar_id):
    pg = ProxyGenerator()

    if not pg.FreeProxies():
        print("FreeProxies fail")
        sys.exit()
    scholarly.use_proxy(pg)

    google_scholar_candidates = []

    try:
        result = scholarly.search_author_id(google_scholar_id)
        google_scholar_candidates.append(result)
        if len(google_scholar_candidates) > 0:
            return google_scholar_candidates[0]
    except:
        print(f"Could not query google with id")


def get_author_by_name_email(name, email):
    # Query pattern: 'John Doe unc.edu'
    query_term = f"{name} {email.split('@')[1]}"
    print(query_term)
    results = []
    try:
        search_query = scholarly.search_author(query_term)
        for i, result in enumerate(search_query):
            results.google_scholar_candidates.append(result)

            if i > 20:
                print(f"Skipping b/c more than 20 results")
                break
    except:
        print(f"Could not query google: {name} with email")


def get_all_details_for_author(author):
    if author:
        try:
            # Retrieve all the details for the author
            return scholarly.fill(author)
        except:
            return None


def get_all_publications(author_details):
    return author_details["publications"]


def get_all_publication_titles(author_details, since_year=0):
    return [
        pub["bib"]["title"]
        for pub in author_details["publications"]
        if "pub_year" in pub["bib"] and int(pub["bib"]["pub_year"]) >= since_year
    ]

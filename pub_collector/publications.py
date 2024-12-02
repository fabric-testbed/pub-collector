from scholarly import scholarly
from scholarly import ProxyGenerator
import sys


def search_publications(pub_title):
    # Search publication by title, return a Publication object
    search_query = scholarly.search_pubs(pub_title)
    return next(search_query)


def get_cited_by(publication):
    publication_filled = scholarly.fill(publication)
    pg = ProxyGenerator()

    if not pg.FreeProxies():
        print("FreeProxies fail")
        sys.exit()
    scholarly.use_proxy(pg)

    citations = [
        citation["bib"]["title"] for citation in scholarly.citedby(publication_filled)
    ]
    return citations

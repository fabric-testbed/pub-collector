from scholarly import scholarly
from scholarly import ProxyGenerator
import sys

from thefuzz import fuzz


def get_first_author(author_name):
    # Retrieve the author's data, fill-in, and print
    # Get an iterator for the author results
    results = scholarly.search_author(author_name)
    # print(list(results))
    # Retrieve the first result from the iterator
    first_author_result = next(results)
    return first_author_result


def search_google_scholar_by_affiliation(name, affiliation, threshold=80):
    """
    Search Google Scholar for a single author using fuzzy matching on affiliation.
    
    Args:
        name (str): The author's full name.
        affiliation (str): Expected affiliation.
        threshold (int): Minimum fuzzy match score (0-100) for affiliation matching.

    Returns:
        str or None: First matching Google Scholar ID, or None if not found.
    """
    try:
        search_query = scholarly.search_author(name)
        
        for author in search_query:
            author_affiliation = author.get('affiliation', '')
            
            if affiliation:
                print(f"Comparing {affiliation} with {author_affiliation}")
                match_score = fuzz.partial_ratio(affiliation.lower(), author_affiliation.lower())
                if match_score < threshold:
                    continue
            
            scholar_id = author.get('scholar_id')
            if scholar_id:
                return scholar_id 
    
    except Exception as e:
        print(f"Error searching for {name}: {e}")
    
    return None


def get_author_by_google_scholar_id(google_scholar_id):
    # pg = ProxyGenerator()

    # if not pg.FreeProxies():
    #     print("FreeProxies fail")
    #     sys.exit()
    # scholarly.use_proxy(pg)

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


def get_all_publications(author_details, since_year=0):
    formatted_publications = []

    for pub in author_details["publications"]:
        bib = pub.get("bib", {})

        # Skip publications that don't have a year or are before since_year
        if "pub_year" not in bib:
            continue

        try:
            pub_year = bib["pub_year"]
            if int(pub_year) < since_year:
                continue
        except ValueError:
            # If pub_year can't be converted to int, skip
            continue

        # Format the citation string
        title = bib.get("title", "")
        venue = bib.get("venue", "")
        pages = bib.get("pages", "")

        # Build citation string
        citation_parts = []
        if venue:
            citation_parts.append(venue)
        if pages:
            citation_parts.append(pages)
        if pub_year:
            citation_parts.append(pub_year)

        citation = ", ".join(citation_parts)

        # Create the formatted publication entry
        formatted_pub = {
            "title": title,
            "pub_year": pub_year,
            "citation": f"{title}, {citation}",
        }

        formatted_publications.append(formatted_pub)

    return formatted_publications


def get_all_publication_titles(author_details, since_year=0):
    return [
        pub["bib"]["title"]
        for pub in author_details["publications"]
        if "pub_year" in pub["bib"] and int(pub["bib"]["pub_year"]) >= since_year
    ]


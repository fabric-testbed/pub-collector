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


def quick_list_author_publications(google_scholar_id, since_year=2020):
    """
    Fetch basic publication information for a given Google Scholar ID
    without filling publication details.

    Parameters:
    - google_scholar_id: The Google Scholar ID
    - since_year: Optional parameter to filter publications after this year (default: 2020)
    """
    try:
        # Search for the author by ID
        author = scholarly.search_author_id(google_scholar_id)

        # Extract basic author info
        name = author.get("name", "")

        # Get publications with basic info only (no fill)
        publications = []
        for pub in scholarly.search_author_pubs(author):
            # Get publication year
            pub_year = pub.get("bib", {}).get("pub_year", "")

            # Skip if publication year is earlier than since_year
            if pub_year and int(pub_year) < since_year:
                continue

            # Extract the basic info we want
            pub_info = {
                "title": pub.get("bib", {}).get("title", ""),
                "pub_year": pub_year,
                "citation": f"{pub.get('bib', {}).get('title', '')}, {pub_year}",
            }
            publications.append(pub_info)

            # Limit to first 10 publications to avoid unnecessary data
            if len(publications) >= 10:
                break

        return {
            "name": name,
            "google_scholar_id": google_scholar_id,
            "publications": publications,
        }

    except Exception as e:
        print(f"Error fetching data for ID {google_scholar_id}: {str(e)}")
        return {
            "name": "Not found",
            "google_scholar_id": google_scholar_id,
            "publications": [],
        }
